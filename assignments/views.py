from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from reports.models import Report, ReportStatusLog
from .models import Assignment, Department
from .forms import AssignmentForm
from notifications.utils import create_notification


def admin_check(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(admin_check)
def assign_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    assignment, created = Assignment.objects.get_or_create(report=report)

    if request.method == 'POST':
        department_id = request.POST.get('department')
        if department_id:
            department = get_object_or_404(Department, id=department_id)
            assignment.department = department
            assignment.assigned_by = request.user
            assignment.save()

            old_status = report.status
            if report.status == 'pending':
                report.status = 'acknowledged'
                report.save()
                ReportStatusLog.objects.create(
                    report=report,
                    old_status=old_status,
                    new_status='acknowledged',
                    changed_by=request.user,
                    notes=f'Assigned to {assignment.department}'
                )

                create_notification(
                    user=report.resident,
                    message=f'Your report "{report.title}" has been assigned and is now being reviewed.',
                    report=report,
                    notif_type='assignment'
                )

            messages.success(request, f'Report assigned to {department.name}!')

    return redirect('admin_report_detail', report_id=report.id)


@login_required
@user_passes_test(admin_check)
def update_status(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        old_status = report.status

        if new_status in dict(Report.STATUS_CHOICES):
            report.status = new_status
            report.save()

            ReportStatusLog.objects.create(
                report=report,
                old_status=old_status,
                new_status=new_status,
                changed_by=request.user,
                notes=notes
            )

            create_notification(
                user=report.resident,
                message=f'Your report "{report.title}" status changed to {report.get_status_display()}.',
                report=report,
                notif_type='status_update'
            )

            messages.success(request, f'Status updated to {report.get_status_display()}')

    return redirect('admin_report_detail', report_id=report.id)


@login_required
@user_passes_test(admin_check)
def add_note(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if request.method == 'POST':
        note = request.POST.get('note')
        if note:
            ReportStatusLog.objects.create(
                report=report,
                old_status=report.status,
                new_status=report.status,
                changed_by=request.user,
                notes=note
            )
            messages.success(request, 'Note added.')

    return redirect('admin_report_detail', report_id=report.id)


@login_required
@user_passes_test(admin_check)
def department_list(request):
    departments = Department.objects.all().order_by('name')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        if name:
            Department.objects.create(name=name, description=description)
            messages.success(request, f'Department "{name}" added.')
            return redirect('department_list')

    return render(request, 'assignments/department_list.html', {'departments': departments})


@login_required
@user_passes_test(admin_check)
def department_delete(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department removed.')
    return redirect('department_list')