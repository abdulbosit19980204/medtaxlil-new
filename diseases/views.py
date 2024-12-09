from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from api.models import Disease, Medication
from .serializers import DiseaseSerializer, MedicationSerializer
from rest_framework.permissions import IsAdminUser
from api.custom_paginator import CustomPagination


class DiseaseViewSet(ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination  # Custom Paginationni qo‘shamiz


class MedicationViewSet(ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination  # Custom Paginationni qo‘shamiz
