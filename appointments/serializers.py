from rest_framework import serializers
from .models import Appointment




class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.first_name')
    doctor_name = serializers.ReadOnlyField(source='doctor.first_name')

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date', 'time', 'reason', 'status', 'patient_name', 'doctor_name']
        read_only_fields = ['status', 'patient', 'doctor']
