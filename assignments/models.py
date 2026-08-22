from django.db import models
from django.contrib.auth.models import User
from reports.models import Report

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='assignment')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_reports')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assignments_made')
    notes = models.TextField(blank=True)
    date_assigned = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.report.title} -> {self.department}"