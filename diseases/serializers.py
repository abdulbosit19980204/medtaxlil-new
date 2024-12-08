from rest_framework import serializers
from api.models import Medication, Disease


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['id', 'name', 'dosage', 'notes', 'disease', 'created_at']
        read_only_fields = ['id', 'created_at']


class DiseaseSerializer(serializers.ModelSerializer):
    medications = MedicationSerializer(many=True, read_only=True)

    class Meta:
        model = Disease
        fields = ['id', 'name', 'symptoms', 'description', 'medications', 'created_at']
        read_only_fields = ['id', 'created_at']
