from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, LoginSerializer

from rest_framework.permissions import IsAuthenticated
from .models import DoctorProfile
from .serializers import DoctorProfileSerializer


User = get_user_model()

# User Registration View
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)


# User Login View
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)


# Doctor Profile Management View
class DoctorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if user.role != 'doctor':
            raise PermissionError("Only doctors can access this.")
        return DoctorProfile.objects.get_or_create(user=user)[0]

# List and Search Doctors
class DoctorListView(generics.ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        specialty = self.request.query_params.get('specialty')
        name = self.request.query_params.get('name')
        if specialty:
            queryset = queryset.filter(specialty__icontains=specialty)
        if name:
            queryset = queryset.filter(user__first_name__icontains=name)
        return queryset
