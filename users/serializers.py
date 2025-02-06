from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .models import CustomUser
from .models import DoctorProfile

CustomUser = get_user_model()

# User Registration Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            # username=validated_data.get('username'),
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data['role'],
        )
        return CustomUser


# User Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        CustomUser = authenticate(email=email, password=password)
        if not CustomUser:
            raise serializers.ValidationError("Invalid credentials.")
        return CustomUser

# Doctor Profile Serializer
class DoctorProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.first_name')

    class Meta:
        model = DoctorProfile
        fields = ['id', 'user', 'username', 'specialty', 'bio', 'availability']
        read_only_fields = ['user']

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = ['id', 'user', 'specialty', 'bio', 'availability']

