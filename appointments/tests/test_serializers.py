from django.test import TestCase
from appointments.serializers import AppointmentSerializer
from users.models import CustomUser
from appointments.models import Appointment

class AppointmentSerializerTestCase(TestCase):
    def setUp(self):
        """Create test patient and doctor"""
        self.patient = CustomUser.objects.create_user(email="patient@example.com", password="pass", role="patient")
        self.doctor = CustomUser.objects.create_user(email="doctor@example.com", password="pass", role="doctor")

    def test_valid_appointment(self):
        """Test if serializer accepts valid appointment data"""
        valid_data = {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
            "date": "2025-02-10",
            "time": "14:00",
            "reason": "Checkup",
            "status": "pending"
        }
        serializer = AppointmentSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_appointment(self):
        """Test if serializer rejects invalid appointment data (missing doctor)"""
        invalid_data = {
            "patient": self.patient.id,
            "date": "2025-02-10",
            "time": "14:00",
            "reason": "Checkup",
            "status": "pending"
        }
        serializer = AppointmentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("doctor", serializer.errors)
