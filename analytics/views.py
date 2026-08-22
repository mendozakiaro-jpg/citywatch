from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, F, ExpressionWrapper, DurationField
from reports.models import Report


def admin_check(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(admin_check)
def analytics_dashboard(request):
    total_reports = Report.objects.count()
    pending_count = Report.objects.filter(status='pending').count()
    in_progress_count = Report.objects.filter(status='in_progress').count()
    resolved_count = Report.objects.filter(status='resolved').count()

    recent_reports = Report.objects.all().order_by('-date_submitted')[:5]

    resolved_reports = Report.objects.filter(status='resolved').annotate(
        resolution_time=ExpressionWrapper(
            F('date_updated') - F('date_submitted'),
            output_field=DurationField()
        )
    )

    avg_resolution = None
    if resolved_reports.exists():
        total_seconds = sum([r.resolution_time.total_seconds() for r in resolved_reports])
        avg_seconds = total_seconds / resolved_reports.count()
        avg_resolution = round(avg_seconds / 86400, 1)

    context = {
        'total_reports': total_reports,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'recent_reports': recent_reports,
        'avg_resolution_days': avg_resolution,
    }

    return render(request, 'analytics/dashboard.html', context)


@login_required
@user_passes_test(admin_check)
def map_view(request):
    reports = Report.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True).order_by('-date_submitted')
    return render(request, 'analytics/map_view.html', {'reports': reports})


@login_required
@user_passes_test(admin_check)
def reports_analytics(request):
    total_reports = Report.objects.count()

    reports_by_category = Report.objects.values('category').annotate(count=Count('id')).order_by('-count')
    reports_by_barangay = Report.objects.values('barangay').annotate(count=Count('id')).order_by('-count')
    reports_by_status = Report.objects.values('status').annotate(count=Count('id')).order_by('-count')

    # add percentage per category for simple bar visualization
    category_data = []
    for item in reports_by_category:
        percent = round((item['count'] / total_reports) * 100, 1) if total_reports else 0
        category_data.append({'label': item['category'], 'count': item['count'], 'percent': percent})

    barangay_data = []
    for item in reports_by_barangay:
        percent = round((item['count'] / total_reports) * 100, 1) if total_reports else 0
        barangay_data.append({'label': item['barangay'], 'count': item['count'], 'percent': percent})

    status_data = []
    for item in reports_by_status:
        percent = round((item['count'] / total_reports) * 100, 1) if total_reports else 0
        status_data.append({'label': item['status'], 'count': item['count'], 'percent': percent})

    resolved_reports = Report.objects.filter(status='resolved').annotate(
        resolution_time=ExpressionWrapper(
            F('date_updated') - F('date_submitted'),
            output_field=DurationField()
        )
    )

    avg_resolution = None
    if resolved_reports.exists():
        total_seconds = sum([r.resolution_time.total_seconds() for r in resolved_reports])
        avg_seconds = total_seconds / resolved_reports.count()
        avg_resolution = round(avg_seconds / 86400, 1)

    context = {
        'total_reports': total_reports,
        'category_data': category_data,
        'barangay_data': barangay_data,
        'status_data': status_data,
        'avg_resolution_days': avg_resolution,
    }

    return render(request, 'analytics/reports_analytics.html', context)