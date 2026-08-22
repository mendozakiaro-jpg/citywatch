from .models import Notification

def create_notification(user, message, report=None, notif_type='general'):
    Notification.objects.create(
        user=user,
        report=report,
        notif_type=notif_type,
        message=message
    )