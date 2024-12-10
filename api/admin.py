from django.contrib import admin
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export import resources
from .models import EKGAnalysis, Patient, CustomUser, Disease, Medication


# CustomUser uchun resurs
class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'gender', 'phone', 'is_active', 'date_joined')


@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin):
    resource_class = CustomUserResource
    list_display = ['username', 'email', 'gender', 'phone', 'is_active']
    search_fields = ['username', 'email', 'phone']
    ordering = ['username']


# Disease uchun resurs
class DiseaseResource(resources.ModelResource):
    class Meta:
        model = Disease
        fields = ('id', 'name', 'symptoms', 'description', 'created_at')


@admin.register(Disease)
class DiseaseAdmin(ImportExportModelAdmin):
    resource_class = DiseaseResource
    list_display = ['name', 'created_at']
    search_fields = ['name', 'symptoms']
    ordering = ['-created_at']


# Medication uchun resurs
class MedicationResource(resources.ModelResource):
    class Meta:
        model = Medication
        fields = ('id', 'name', 'disease__name', 'dosage', 'notes', 'created_at')


@admin.register(Medication)
class MedicationAdmin(ImportExportModelAdmin):
    resource_class = MedicationResource
    list_display = ['name', 'disease', 'dosage', 'created_at']
    search_fields = ['name', 'disease__name']
    ordering = ['-created_at']


# Patient uchun resurs
class PatientResource(resources.ModelResource):
    class Meta:
        model = Patient
        fields = ('id', 'full_name', 'age', 'gender', 'user__username', 'phone', 'complaints', 'created_at')


@admin.register(Patient)
class PatientAdmin(ImportExportModelAdmin):
    resource_class = PatientResource
    list_display = ['full_name', 'age', 'gender', 'user', 'created_at']
    search_fields = ['full_name', 'phone']
    ordering = ['-created_at']


# EKGAnalysis uchun resurs
class EKGAnalysisResource(resources.ModelResource):
    class Meta:
        model = EKGAnalysis
        fields = ('id', 'patient__full_name', 'image', 'diagnosis', 'recommended_medicine', 'uploaded_at')


@admin.register(EKGAnalysis)
class EKGAnalysisAdmin(ImportExportModelAdmin):
    resource_class = EKGAnalysisResource
    list_display = ['patient', 'uploaded_at', 'diagnosis']
    search_fields = ['patient__full_name', 'diagnosis']
    ordering = ['-uploaded_at']
