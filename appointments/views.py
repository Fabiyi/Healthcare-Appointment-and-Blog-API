from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Appointment
from .serializers import AppointmentSerializer




class AppointmentListCreateAPIView(generics.ListCreateAPIView):
    """Allows patients to create appointments and doctors/patients to view them"""
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Patients see their appointments, doctors see assigned appointments"""
        user = self.request.user
        if user.role == 'patient':
            return Appointment.objects.filter(patient=user)
        elif user.role == 'doctor':
            return Appointment.objects.filter(doctor=user)
        return Appointment.objects.none()

    def perform_create(self, serializer):
        """Ensure that only patients can book appointments"""
        if self.request.user.role != 'patient':
            raise PermissionDenied("Only patients can create appointments.")
        serializer.save(patient=self.request.user)

#         A. Book an Appointment (Patients Only)

# URL: POST http://127.0.0.1:8000/appointments/

# Headers:

# Authorization: Bearer <JWT_ACCESS_TOKEN>

# Body (JSON):

# {
#   "doctor": 2,
#   "date": "2025-03-10",
#   "time": "15:00",
#   "reason": "Routine checkup"
# }

# ✅ Success Response (201 Created):

# {
#   "id": 1,
#   "patient_email": "patient@example.com",
#   "doctor_name": "Dr. John Doe",
#   "doctor": 2,
#   "date": "2025-03-10",
#   "time": "15:00",
#   "reason": "Routine checkup",
#   "status": "pending"
# }


class AppointmentUpdateAPIView(generics.UpdateAPIView):
    """Allows doctors to update appointment status"""
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """Doctors can accept/decline appointments"""
        appointment = self.get_object()

        if request.user.role != 'doctor':
            raise PermissionDenied("Only doctors can update appointment status.")

        new_status = request.data.get('status')
        if new_status not in ['accepted', 'declined']:
            return Response({"error": "Invalid status update"}, status=400)

        appointment.status = new_status
        appointment.save()
        return Response({"id": appointment.id, "status": appointment.status})
    
# B. View Appointments (Patients & Doctors)

# URL: GET http://127.0.0.1:8000/api/appointments/

# ✅ Success Response (200 OK):

# [
#   {
#     "id": 1,
#     "patient_email": "patient@example.com",
#     "doctor_name": "Dr. John Doe",
#     "doctor": 2,
#     "date": "2025-03-10",
#     "time": "15:00",
#     "reason": "Routine checkup",
#     "status": "pending"
#   }
# ]

# C. Update Appointment Status (Doctors Only)

# URL: PATCH http://127.0.0.1:8000/api/appointments/1/

# Headers:

# Authorization: Bearer <JWT_ACCESS_TOKEN>

# Body (JSON):

# {
#   "status": "accepted"
# }

# ✅ Success Response (200 OK):

# {
#   "id": 1,
#   "status": "accepted"
# }



class AppointmentCancelAPIView(generics.UpdateAPIView):
    """Allows patients or doctors to cancel appointments"""
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """Handle appointment cancellation"""
        appointment = self.get_object()
        user = request.user

        if user.role == 'patient' and appointment.patient != user:
            raise PermissionDenied("You can only cancel your own appointments.")
        if appointment.status in ['accepted', 'declined', 'canceled']:
            return Response({"error": "This appointment cannot be canceled."}, status=400)

        appointment.status = 'canceled'
        appointment.save()
        return Response({"id": appointment.id, "status": appointment.status})


# A. Cancel an Appointment (Patients or Doctors)

# URL: PATCH http://127.0.0.1:8000/api/appointments/1/cancel/

# Headers:

# Authorization: Bearer <JWT_ACCESS_TOKEN>

# ✅ Success Response (200 OK):

# {
#   "id": 1,
#   "status": "canceled"
# }

# ❌ Error Responses:

# If trying to cancel someone else's appointment (for patients).


