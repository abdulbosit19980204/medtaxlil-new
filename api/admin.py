from django import forms
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from .models import CustomUser, Disease, Medication, Patient, EKGAnalysis


# Parolni o'zgartirish formasi
class CustomUserChangePasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Enter new password')}),
        label=_("New Password"),
        max_length=128
    )


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

    # Parolni avtomatik hashlash
    def save_model(self, request, obj, form, change):
        if not change or ('password' in form.changed_data):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

    # Parolni almashtirish action'ini qo'shish
    def change_password(self, request, user_id):
        from django.shortcuts import get_object_or_404, render, redirect
        user = get_object_or_404(CustomUser, pk=user_id)

        if request.method == 'POST':
            form = CustomUserChangePasswordForm(request.POST)
            if form.is_valid():
                user.password = make_password(form.cleaned_data['password'])
                user.save()
                self.message_user(request, _("Password changed successfully."))
                return redirect(f'/admin/{self.model._meta.app_label}/{self.model._meta.model_name}/{user_id}/change/')
        else:
            form = CustomUserChangePasswordForm()

        context = {
            'form': form,
            'opts': self.model._meta,
            'title': _("Change Password for %s") % user.username,
            'is_popup': False,
            'save_as': False,
            'has_view_permission': True,
            'has_change_permission': True,
        }
        return render(request, 'admin/change_password.html', context)

    # Custom action uchun URL qo'shish
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/change_password/', self.admin_site.admin_view(self.change_password),
                 name='change_password'),
        ]
        return custom_urls + urls


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
    disease = Field(
        column_name='disease__name',
        attribute='disease',
        widget=ForeignKeyWidget(Disease, 'name')
    )

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
    user = Field(attribute='user__username', column_name='user__username')

    class Meta:
        model = Patient
        fields = ('id', 'full_name', 'age', 'gender', 'user', 'phone', 'complaints', 'created_at')


@admin.register(Patient)
class PatientAdmin(ImportExportModelAdmin):
    resource_class = PatientResource
    list_display = ['full_name', 'age', 'gender', 'user', 'created_at']
    search_fields = ['full_name', 'phone']
    ordering = ['-created_at']


# EKGAnalysis uchun resurs
class EKGAnalysisResource(resources.ModelResource):
    patient = Field(attribute='patient__full_name', column_name='patient__full_name')

    class Meta:
        model = EKGAnalysis
        fields = ('id', 'patient', 'image', 'diagnosis', 'recommended_medicine', 'uploaded_at')


@admin.register(EKGAnalysis)
class EKGAnalysisAdmin(ImportExportModelAdmin):
    resource_class = EKGAnalysisResource
    list_display = ['patient', 'uploaded_at', 'diagnosis']
    search_fields = ['patient__full_name', 'diagnosis']
    ordering = ['-uploaded_at']
