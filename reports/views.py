from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Report, ReportStatusLog, ReportFeedback
from .forms import ReportForm, ReportFeedbackForm
from notifications.utils import create_notification


def admin_check(user):
    return user.is_staff or user.is_superuser


@login_required
def resident_dashboard(request):
    reports = Report.objects.filter(resident=request.user)
    active_reports = reports.exclude(status__in=['resolved', 'closed']).order_by('-date_submitted')[:5]

    stats = {
        'total': reports.count(),
        'pending': reports.filter(status='pending').count(),
        'in_progress': reports.filter(status='in_progress').count(),
        'resolved': reports.filter(status='resolved').count(),
    }

    return render(request, 'reports/dashboard.html', {
        'reports': active_reports,
        'stats': stats,
    })


@login_required
def report_list(request):
    reports = Report.objects.filter(resident=request.user)
    status_filter = request.GET.get('status')
    if status_filter:
        reports = reports.filter(status=status_filter)

    stats = {
        'total': reports.count(),
        'pending': reports.filter(status='pending').count(),
        'in_progress': reports.filter(status='in_progress').count(),
        'resolved': reports.filter(status='resolved').count(),
    }

    return render(request, 'reports/report_list.html', {'reports': reports, 'stats': stats, 'status_filter': status_filter})


@login_required
def report_create(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.resident = request.user
            report.save()

            ReportStatusLog.objects.create(
                report=report,
                old_status='',
                new_status='pending',
                changed_by=request.user,
                notes='Report submitted'
            )

            create_notification(
                user=request.user,
                message=f'Your report "{report.title}" has been submitted.',
                report=report,
                notif_type='status_update'
            )

            messages.success(request, 'Report submitted successfully!')
            return redirect('report_detail', report_id=report.id)
        else:
            messages.error(request, 'Please check the form for errors.')
    else:
        form = ReportForm()

    return render(request, 'reports/report_form.html', {'form': form})


@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if report.resident != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to view this report.")
        return redirect('report_list')

    status_logs = report.status_logs.all()
    feedback = getattr(report, 'feedback', None)
    feedback_form = None

    if report.status == 'resolved' and not feedback:
        feedback_form = ReportFeedbackForm()

    if request.method == 'POST' and report.status == 'resolved' and not feedback:
        feedback_form = ReportFeedbackForm(request.POST)
        if feedback_form.is_valid():
            fb = feedback_form.save(commit=False)
            fb.report = report
            fb.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('report_detail', report_id=report.id)

    return render(request, 'reports/report_detail.html', {
        'report': report,
        'status_logs': status_logs,
        'feedback': feedback,
        'feedback_form': feedback_form,
    })


@login_required
def report_edit(request, report_id):
    report = get_object_or_404(Report, id=report_id, resident=request.user)

    if report.status != 'pending':
        messages.error(request, 'You can only edit reports that are still pending.')
        return redirect('report_detail', report_id=report.id)

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated successfully!')
            return redirect('report_detail', report_id=report.id)
    else:
        form = ReportForm(instance=report)

    return render(request, 'reports/report_form.html', {'form': form, 'editing': True})


@login_required
def report_delete(request, report_id):
    report = get_object_or_404(Report, id=report_id, resident=request.user)

    if report.status != 'pending':
        messages.error(request, 'You can only delete reports that are still pending.')
        return redirect('report_detail', report_id=report.id)

    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Report deleted.')
        return redirect('report_list')

    return render(request, 'reports/report_confirm_delete.html', {'report': report})


def public_board(request):
    reports = Report.objects.all().order_by('-date_submitted')

    status_filter = request.GET.get('status')
    category_filter = request.GET.get('category')

    if status_filter:
        reports = reports.filter(status=status_filter)
    if category_filter:
        reports = reports.filter(category=category_filter)

    total_reports = Report.objects.count()
    resolved_count = Report.objects.filter(status='resolved').count()

    return render(request, 'reports/public_board.html', {
        'reports': reports[:20],
        'total_reports': total_reports,
        'resolved_count': resolved_count,
    })


@login_required
@user_passes_test(admin_check)
def admin_report_list(request):
    reports = Report.objects.all().order_by('-date_submitted')

    status_filter = request.GET.get('status')
    category_filter = request.GET.get('category')
    search_query = request.GET.get('q')

    if status_filter:
        reports = reports.filter(status=status_filter)
    if category_filter:
        reports = reports.filter(category=category_filter)
    if search_query:
        reports = reports.filter(title__icontains=search_query)

    return render(request, 'reports/admin_report_list.html', {
        'reports': reports,
        'status_filter': status_filter,
        'category_filter': category_filter,
    })


@login_required
@user_passes_test(admin_check)
def admin_report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    status_logs = report.status_logs.all()
    assignment = getattr(report, 'assignment', None)

    from assignments.models import Department
    departments = Department.objects.all()

    return render(request, 'reports/admin_report_detail.html', {
        'report': report,
        'status_logs': status_logs,
        'assignment': assignment,
        'departments': departments,
    })