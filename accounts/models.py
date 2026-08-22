from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('resident', 'Resident'),
        ('admin', 'Admin/LGU Staff'),
        ('personnel', 'Field Personnel'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='resident')
    phone_number = models.CharField(max_length=20, blank=True)
    barangay = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    def is_admin(self):
        return self.role == 'admin'

    def is_personnel(self):
        return self.role == 'personnel'

    def is_resident(self):
        return self.role == 'resident'