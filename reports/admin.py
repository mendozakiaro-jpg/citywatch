from django.contrib import admin
from .models import Report, ReportStatusLog, ReportFeedback

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'resident', 'category', 'status', 'urgency', 'barangay', 'date_submitted']
    list_filter = ['status', 'category', 'urgency', 'barangay']
    search_fields = ['title', 'description', 'resident__username']

admin.site.register(ReportStatusLog)
admin.site.register(ReportFeedback)