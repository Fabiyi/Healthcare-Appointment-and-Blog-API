from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, LoginSerializer

from rest_framework.permissions import IsAuthenticated
from .models import DoctorProfile
from .serializers import DoctorProfileSerializer

from rest_framework import generics, permissions


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
            "message": "User registered successfully."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

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
    
    





class DoctorProfileCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Check if the logged-in user is a doctor
        if self.request.user.role != 'doctor':
            raise PermissionDenied("Only doctors can create or update a profile.")
        
        # Save the doctor profile linked to the logged-in user
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Check if the logged-in user is a doctor
        if self.request.user.role != 'doctor':
            raise PermissionDenied("Only doctors can create or update a profile.")
        
        # Update the doctor profile
        serializer.save()
    
    




class DoctorProfileListView(generics.ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.AllowAny]



class DoctorProfileSearchView(generics.ListAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = DoctorProfile.objects.all()
        specialty = self.request.query_params.get('specialty')
        name = self.request.query_params.get('name')
        if specialty:
            queryset = queryset.filter(specialty__icontains=specialty)
        if name:
            queryset = queryset.filter(user__first_name__icontains=name) | queryset.filter(user__last_name__icontains=name)
        return queryset
    
   