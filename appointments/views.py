from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Appointment
from .serializers import AppointmentSerializer


# Create your views here.


class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)
# Create an Appointment

# (URL: /appointments/ ) ........   (Method: POST) ........   ( Role Required: Patient)

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


class AppointmentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == 'patient':
            appointments = Appointment.objects.filter(patient=user)
        elif user.role == 'doctor':
            appointments = Appointment.objects.filter(doctor=user)
        else:
            return Response({"detail": "Invalid user role."}, status=403)

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

# ...................View Appointments
# (URL: /appointments/) ...........      ( Method: GET)  
#        (Description: View all appointments for the logged-in user (doctor or patient).)

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




class AppointmentUpdateView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        appointment = self.get_object()
        if request.user != appointment.doctor:
            return Response({"detail": "Only the doctor can update this appointment."}, status=403)
        return super().partial_update(request, *args, **kwargs)

#.......................................... Update Appointment Status
# (URL: /appointments/<id>/) ..................  (Method: PATCH) ............(Role Required: Doctor)

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



