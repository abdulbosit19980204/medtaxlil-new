from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import CustomUser, Disease, Medication, Patient, EKGAnalysis


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
    # Create a ForeignKeyWidget for the disease field
    disease = fields.Field(
        column_name='disease__name',
        attribute='disease',
        widget=ForeignKeyWidget(Disease, 'name')
    )

    class Meta:
        model = Medication
        fields = ('id', 'name', 'disease__name', 'dosage', 'notes', 'created_at')

    def before_import_row(self, row, **kwargs):
        disease_name = row.get('disease__name')
        if disease_name:
            disease = Disease.objects.filter(name=disease_name).first()
            if disease:
                row['disease'] = disease  # Assign the Disease instance
            else:
                raise ValueError(f"Disease '{disease_name}' does not exist. Please add it to the database first.")
        else:
            raise ValueError("The 'disease__name' field is missing in the row.")


@admin.register(Medication)
class MedicationAdmin(ImportExportModelAdmin):
    resource_class = MedicationResource
    list_display = ['name', 'disease', 'dosage', 'created_at']
    search_fields = ['name', 'disease__name']
    ordering = ['-created_at']


# Patient uchun resurs
class PatientResource(resources.ModelResource):
    user__username = fields.Field(attribute='user__username', column_name='user__username')

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
    patient__full_name = fields.Field(attribute='patient__full_name', column_name='patient__full_name')

    class Meta:
        model = EKGAnalysis
        fields = ('id', 'patient__full_name', 'image', 'diagnosis', 'recommended_medicine', 'uploaded_at')


@admin.register(EKGAnalysis)
class EKGAnalysisAdmin(ImportExportModelAdmin):
    resource_class = EKGAnalysisResource
    list_display = ['patient', 'uploaded_at', 'diagnosis']
    search_fields = ['patient__full_name', 'diagnosis']
    ordering = ['-uploaded_at']
