from django.contrib import admin
from .models import EKGAnalysis, Patient, CustomUser, Disease, Medication

admin.site.register(EKGAnalysis)
admin.site.register(CustomUser)


# admin.site.register(Patient)


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'symptoms']
    ordering = ['created_at']


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'disease', 'created_at']
    search_fields = ['name', 'disease__name']
    ordering = ['created_at']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'age', 'gender')
