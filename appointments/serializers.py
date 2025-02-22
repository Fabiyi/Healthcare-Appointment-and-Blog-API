from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    patient_email = serializers.EmailField(source='patient.email', read_only=True)
    doctor_name = serializers.CharField(source='doctor.first_name', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient_email', 'doctor_name', 'doctor', 'date', 'time', 'reason', 'status']
        read_only_fields = ['status']

    def validate_status(self, value):
        """Ensure only valid status updates"""
        if value not in ['accepted', 'declined', 'canceled']:
            raise serializers.ValidationError("Invalid status update.")
        return value
