from rest_framework import serializers
from api.models import Patient, EKGAnalysis, Medication
from diseases.serializers import DiseaseSerializer
from ekg.serializers import EKGAnalysisSerializer


class PatientSerializer(serializers.ModelSerializer):
    predicted_disease = DiseaseSerializer(read_only=True)
    ekg_images = EKGAnalysisSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()  # Custom field for a single image or default image

    class Meta:
        model = Patient
        fields = ['id', 'user', 'full_name', 'phone', 'age', 'gender', 'complaints', 'created_at', 'predicted_disease',
                  'analysis_notes', 'ekg_images', 'image']
        read_only_fields = ['id', 'user', 'predicted_disease', 'analysis_notes', 'created_at', 'ekg_images', 'image']

    def get_image(self, obj):
        """
        Returns the first associated EKG image or a default image URL.
        """
        first_ekg = obj.ekg_images.first()  # Fetch the first related EKGAnalysis object
        if first_ekg and first_ekg.image:
            return first_ekg.image.url  # Return the URL of the first image
        return '/media/ekg_images/default.jpg'  # Replace with your actual default image path


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
