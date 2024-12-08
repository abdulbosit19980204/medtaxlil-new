from rest_framework import serializers
from api.models import  EKGAnalysis




class EKGAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = EKGAnalysis
        fields = '__all__'
