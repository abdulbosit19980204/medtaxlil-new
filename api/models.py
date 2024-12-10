from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    gender = models.CharField(_('Gender'), max_length=10, choices=[('male', _('Male')), ('female', _('Female'))])
    image = models.ImageField(upload_to='users/pictures/', default='/users/pictures/default.jpg')
    phone = models.CharField(_('Phone'), max_length=11, blank=True, null=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Disease(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    symptoms = models.TextField(_('Symptoms'))
    description = models.TextField(_('Description'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Disease')
        verbose_name_plural = _('Diseases')


class Medication(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(_('Name'), max_length=255)
    dosage = models.CharField(_('Dosage'), max_length=255)
    notes = models.TextField(_('Notes'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (for {self.disease.name})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Medication')
        verbose_name_plural = _('Medications')


class Patient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patients')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(_('Phone number'), max_length=13, blank=True, null=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('male', _('Male')), ('female', _('Female'))])
    complaints = models.TextField(_('Complaints'))
    predicted_disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True)
    analysis_notes = models.TextField(_('Analysis Notes'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.age} years)"

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Patient')
        verbose_name_plural = _('Patients')


class EKGAnalysis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='ekg_images')
    image = models.ImageField(upload_to='ekg_images/')
    analysis_data = models.JSONField(blank=True, null=True)
    diagnosis = models.CharField(_('Diagnosis'), max_length=255, blank=True, null=True)
    recommended_medicine = models.TextField(_('Recommended Medicine'), blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.full_name} {self.uploaded_at}"

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = _('EKG Analysis')
        verbose_name_plural = _('EKG Analyses')
