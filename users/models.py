from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import CustomUserManager
# Create your models here.


# Create (CUSTOM USER MODEL) a user model that adds roles (like "patient" or "doctor") 
# two .......... types of (ACUSTOM USER MODEL) class or AbstractBase class
# 1..... AbstractUser class: It allows you to add to what django provided extra fields.
# 2......AbstractBase class: It allows you to build your user from scratch.

# class CustomUser(AbstractUser):
#     ROLE_CHOICES = [
#         ('patient', 'Patient'),
#         ('doctor', 'Doctor'),
#     ]
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)




class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with email as the username field and role-based access.
    """
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role})"


class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_profile")
    specialty = models.CharField(max_length=255)
    bio = models.TextField(blank=True,)
    availability = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.specialty}"