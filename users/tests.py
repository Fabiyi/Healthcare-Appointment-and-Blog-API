from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import DoctorProfile


# Create your tests here.


User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.doctor = User.objects.create_user(
            email="doctor@example.com", password="password", role="doctor"
        )
        self.patient = User.objects.create_user(
            email="patient@example.com", password="password", role="patient"
        )

    def test_register_user(self):
        response = self.client.post('/auth/register/', {
            "email": "newuser@example.com",
            "password": "password",
            "role": "patient",
            "first_name": "John",
            "last_name": "Doe"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_doctor_profile_creation(self):
        self.client.force_authenticate(user=self.doctor)
        response = self.client.post('/users/doctors/manage/', {
            "specialty": "Cardiology",
            "bio": "Experienced Cardiologist",
            "availability": "Mon-Fri, 9 AM - 3 PM"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DoctorProfile.objects.count(), 1)
