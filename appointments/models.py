from django.db import models
from django.conf import settings


# Create your models here.

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_as_patient',null=True,  # Allow null
    blank=True  # Allow forms to leave it empty
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_as_doctor',null=True,  # Allow null
    blank=True  # Allow forms to leave it empty
    )
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Appointment with {self.doctor.first_name} on {self.date} at {self.time}"


