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

# a. User Authentication Endpoints (doctor or patient)

# User Registration View
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
    
    
    

# 1.1. Register a User
# URL: auth/register/
# Method: POST
# Description: Register a new user as either a patient or doctor.

# ............Request Body Example:

# {
#   "email": "doctor1@example.com",
#   "password": "securepassword",
#   "first_name": "John",
#   "last_name": "Doe",
#   "role": "doctor"
# }

# ............Response Example:
# {
#   "id": 1,
#   "email": "doctor1@example.com",
#   "first_name": "John",
#   "last_name": "Doe",
#   "role": "doctor"
# }






# ...... Login a User ......(URL: users/login/ ) ......(Method: POST).... (Description: Authenticate a user and get a JSON Web Token (JWT).)
# User Login View
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
    
    
    
### ......... Request Body Example

# {
#   "email": "doctor1@example.com",
#   "password": "securepassword"
# }

### .......... Response Example
# {
#   "access": "jwt_access_token",
#   "refresh": "jwt_refresh_token"
# }


#........................................ Doctor Management Endpoints
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
    
    
# Create View and Update ( Doctor  Mnanagement)

# Create/Update a Doctor Profile
# URL: users/doctors/
# Method: POST (if creating) or PATCH (if updating)
# Role Required: Doctor
# Description: Create or update a doctor’s profile.


##   (Request):

# {
#   "specialty": "Cardiology",
#   "bio": "Experienced cardiologist with 10+ years of expertise.",
#   "availability": "Monday to Friday, 9 AM to 5 PM"
# }
##   (Response):

# {
#   "id": 1,
#   "user": "doctor1@example.com",
#   "specialty": "Cardiology",
#   "bio": "Experienced cardiologist with 10+ years of expertise.",
#   "availability": "Monday to Friday, 9 AM to 5 PM"
# }




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
    
    
### Retrieve a List of Doctors
# (URL: users/doctors/ ) ......   (Method: GET)  ......   (Description: Retrieve a list of all doctors.)
                                # ........Response:

# [
#   {
#     "id": 1,
#     "name": "Dr. John Doe",
#     "specialty": "Cardiology",
#     "bio": "Experienced cardiologist with 10+ years of expertise.",
#     "availability": "Monday to Friday, 9 AM to 5 PM"
#   },
#   {
#     "id": 2,
#     "name": "Dr. Jane Smith",
#     "specialty": "Neurology",
#     "bio": "Specialist in neurological disorders.",
#     "availability": "Monday to Thursday, 10 AM to 4 PM"
#   }
# ]



class DoctorProfileListView(generics.ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.AllowAny]

### Search for Doctors
# (URL: users/doctors/search/)  ........    (Method: GET) ...... (Description: Search for doctors by name or specialty.)
                           # (Query Parameters Example: /doctors/search/?specialty=Cardiology)


# ...........Response
# [
#   {
#     "id": 1,
#     "name": "Dr. John Doe",
#     "specialty": "Cardiology",
#     "bio": "Experienced cardiologist with 10+ years of expertise.",
#     "availability": "Monday to Friday, 9 AM to 5 PM"
#   }
# ]

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
    
   