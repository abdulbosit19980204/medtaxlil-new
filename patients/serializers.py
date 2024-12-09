from rest_framework import serializers
from api.models import Patient, EKGAnalysis, Medication
from diseases.serializers import DiseaseSerializer


class PatientSerializer(serializers.ModelSerializer):
    predicted_disease = DiseaseSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'user', 'full_name', 'phone', 'age', 'gender', 'complaints', 'created_at', 'predicted_disease',
                  'analysis_notes']
        read_only_fields = ['id', 'user', 'predicted_disease', 'analysis_notes', 'created_at']


class PrescriptionSerializer(serializers.ModelSerializer):
    disease_name = serializers.CharField(source='patient.predicted_disease.name', read_only=True)
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    medications = serializers.SerializerMethodField()

    class Meta:
        model = EKGAnalysis
        fields = ['id', 'patient_name', 'disease_name', 'recommended_medicine', 'medications']

    def get_medications(self, obj):
        if obj.patient.predicted_disease:
            medications = Medication.objects.filter(disease=obj.patient.predicted_disease)
            return [
                {"name": med.name, "dosage": med.dosage} for med in medications
            ]
        return []
