from django.test import TestCase
from users.models import CustomUser

class CustomUserTestCase(TestCase):
    def setUp(self):
        """Set up test data before each test"""
        self.user = CustomUser.objects.create_user(
            email="patient@example.com",
            password="testpass123",
            role="patient"
        )

    def test_user_creation(self):
        """Check if user is created correctly"""
        self.assertEqual(self.user.email, "patient@example.com")
        self.assertTrue(self.user.check_password("testpass123"))
        self.assertEqual(self.user.role, "patient")

    def test_superuser_creation(self):
        """Check if superuser is created correctly"""
        admin = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
