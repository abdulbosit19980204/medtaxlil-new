from rest_framework import serializers
from api.models import Patient
from diseases.serializers import DiseaseSerializer


class PatientSerializer(serializers.ModelSerializer):
    predicted_disease = DiseaseSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'user', 'full_name', 'age', 'gender', 'complaints', 'created_at', 'predicted_disease',
                  'analysis_notes']
        read_only_fields = ['id', 'user', 'predicted_disease', 'analysis_notes', 'created_at']
