from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from appointments.models import Appointment

class AppointmentTestCase(APITestCase):
    def setUp(self):
        """Create a test patient and doctor"""
        self.patient = CustomUser.objects.create_user(
            email="patient@example.com",
            password="patientpass",
            role="patient"
        )
        self.doctor = CustomUser.objects.create_user(
            email="doctor@example.com",
            password="doctorpass",
            role="doctor"
        )
        self.client.login(email="patient@example.com", password="patientpass")
        self.create_appointment_url = reverse('appointment-list')  # Update with actual endpoint

    def test_create_appointment(self):
        """Check if a patient can book an appointment"""
        data = {
            "doctor": self.doctor.id,
            "date": "2025-02-05",
            "time": "14:30",
            "reason": "Regular Checkup"
        }
        response = self.client.post(self.create_appointment_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "pending")
