from django.db import models
from users.models import CustomUser  # Import your custom user model

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('canceled', 'Canceled'),
    ]

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="doctor_appointments", null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.first_name} on {self.date} at {self.time}"
