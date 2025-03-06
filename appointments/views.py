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





