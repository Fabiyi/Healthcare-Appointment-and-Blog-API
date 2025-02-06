from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Appointment
from .serializers import AppointmentSerializer


# Create your views here.


# Create Appointment (Patients Only)
class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'patient':
            raise PermissionDenied("Only patients can book appointments.")
        serializer.save(patient=self.request.user)

# Create an Appointment (PATIENT ONLY & VIEW THIER APPOINTMENT)

# (URL: /appointments/ ) 
# ........   (Method: POST) ........   ( Role Required: Patient)

# (Request):

# {
#   "id": 1,
#   "patient": "patient1@example.com",
#   "doctor": "Dr. John Doe",
#   "date": "2025-02-01",
#   "time": "14:00",
#   "status": "pending",
#   "reason": "Routine check-up"
# }


# List Appointments (Doctors or Patients)
class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'doctor':
            return Appointment.objects.filter(doctor=user)
        elif user.role == 'patient':
            return Appointment.objects.filter(patient=user)
        raise PermissionDenied("Invalid role.")


# ...................View Appointments(DOCTOR ONLY SEE APPOINTMENT ASSIGNED TO THEM)
# (URL: /appointments/list/) ...........      
# ( Method: GET)  
#        (Description: View all appointments for the logged-in user (doctor "PATCH" or patient "GET").)

# (Response):
# [
#   {
#     "id": 1,
#     "patient": "patient1@example.com",
#     "date": "2025-02-01",
#     "time": "14:00",
#     "status": "pending",
#     "reason": "Routine check-up"
#   }
# ]




# Update Appointment Status (Doctors Only)
class AppointmentUpdateView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        appointment = self.get_object()
        if self.request.user != appointment.doctor:
            raise PermissionDenied("Only the assigned doctor can update the appointment.")
        serializer.save()


#................................... Update Appointment Status (DOCTOR UPDATE THE APPOINTMENT STATUS)
# (URL: /appointments/<id>/) ..................  
# (Method: PATCH) ............(Role Required: Doctor)

# (Request):
# {
#   "status": "accepted"
# }

#(Response):
# {
#   "id": 1,
#   "patient": "patient1@example.com",
#   "doctor": "Dr. John Doe",
#   "date": "2025-02-01",
#   "time": "14:00",
#   "status": "accepted",
#   "reason": "Routine check-up"
# }



