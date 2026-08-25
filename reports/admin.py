from django.contrib import admin
from .models import Announcement, Report, ReportStatusLog, ReportFeedback


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'announcement_type', 'is_published', 'date_published']
    list_filter = ['announcement_type', 'is_published']
    search_fields = ['title', 'content']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'resident', 'category', 'status', 'urgency', 'barangay', 'date_submitted']
    list_filter = ['status', 'category', 'urgency', 'barangay']
    search_fields = ['title', 'description', 'resident__username']

admin.site.register(ReportStatusLog)
admin.site.register(ReportFeedback)