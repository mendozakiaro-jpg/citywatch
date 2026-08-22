from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    CATEGORY_CHOICES = [
        ('road', 'Road'),
        ('streetlight', 'Streetlight'),
        ('drainage', 'Drainage/Flooding'),
        ('facility', 'Public Facility'),
        ('other', 'Others'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    URGENCY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='low')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    photo = models.ImageField(upload_to='report_photos/', blank=True, null=True)
    barangay = models.CharField(max_length=100)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_submitted']

    def __str__(self):
        return f"{self.title} ({self.status})"


class ReportStatusLog(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='status_logs')
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.report.title}: {self.old_status} -> {self.new_status}"


class ReportFeedback(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.report.title} - {self.rating} stars"