from django.db import models
from django.contrib.auth.models import User
from reports.models import Report

class Notification(models.Model):
    NOTIF_TYPE_CHOICES = [
        ('status_update', 'Status Update'),
        ('assignment', 'Assignment'),
        ('feedback_request', 'Feedback Request'),
        ('general', 'General'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=True)
    notif_type = models.CharField(max_length=20, choices=NOTIF_TYPE_CHOICES, default='general')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.user.username}: {self.message[:30]}"