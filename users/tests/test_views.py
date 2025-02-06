from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class UserAuthenticationTestCase(APITestCase):
    def setUp(self):
        """Create a test user"""
        self.user = User.objects.create_user(
            email="doctor@example.com",
            password="securepass",
            role="doctor"
        )
        self.login_url = reverse('login')  # Update with actual login endpoint name

    def test_user_registration(self):
        """Test if users can register"""
        url = reverse('register')  # Update with actual register endpoint name
        data = {
            "email": "newpatient@example.com",
            "password": "newpassword123",
            "role": "patient"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], "newpatient@example.com")

    def test_user_login(self):
        """Test if users can log in"""
        data = {
            "email": "doctor@example.com",
            "password": "securepass"
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # Check if token is returned
