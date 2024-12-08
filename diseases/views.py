from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from api.models import Disease, Medication
from .serializers import DiseaseSerializer, MedicationSerializer
from rest_framework.permissions import IsAdminUser


class DiseaseViewSet(ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [IsAdminUser]


class MedicationViewSet(ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsAdminUser]
