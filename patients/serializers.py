from rest_framework import serializers
from api.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'user', 'full_name', 'age', 'gender', 'complaints', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
