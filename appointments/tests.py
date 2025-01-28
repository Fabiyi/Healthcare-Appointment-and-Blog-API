from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Appointment

# Create your tests here.



User = get_user_model()

class AppointmentTests(APITestCase):
    def setUp(self):
        self.doctor = User.objects.create_user(
            email="doctor@example.com", password="password", role="doctor"
        )
        self.patient = User.objects.create_user(
            email="patient@example.com", password="password", role="patient"
        )

    def test_create_appointment(self):
        self.client.force_authenticate(user=self.patient)
        response = self.client.post('/appointments/', {
            "doctor": self.doctor.id,
            "date": "2025-01-21",
            "time": "14:00:00",
            "reason": "Consultation"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
