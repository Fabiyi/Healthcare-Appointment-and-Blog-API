from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.




class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_profile")
    specialty = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.specialty}"