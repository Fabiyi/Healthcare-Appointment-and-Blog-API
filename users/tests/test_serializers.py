from django.test import TestCase
from users.serializers import UserSerializer
from users.models import CustomUser

class UserSerializerTestCase(TestCase):
    def test_valid_user_data(self):
        """Test if serializer accepts valid user data"""
        valid_data = {
            "email": "patient@example.com",
            "password": "securepass",
            "role": "patient",
        }
        serializer = UserSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["email"], "patient@example.com")
    
    def test_invalid_user_data(self):
        """Test if serializer rejects missing email"""
        invalid_data = {
            "password": "securepass",
            "role": "patient",
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
