from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    gender = models.CharField(_('Gender'), max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    image = models.ImageField(upload_to='users/pictures/', default='/users/pictures/default.jpg')
    phone = models.CharField(_('Phone'), max_length=11, blank=True, null=True)


class Disease(models.Model):
    name = models.CharField(_('Name'), max_length=255)  # Kasallik nomi
    symptoms = models.TextField(_('Symptoms'))  # Kasallik belgilari
    description = models.TextField(_('Description'))  # Kasallik haqida batafsil ma'lumot
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Medication(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(_('Name'), max_length=255)  # Dori nomi
    dosage = models.CharField(_('Dosage'), max_length=255)  # Qabul qilish dozalari
    notes = models.TextField(_('Notes'), blank=True, null=True)  # Qo'shimcha ma'lumot
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (for {self.disease.name})"


class Patient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patients')
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    complaints = models.TextField()  # Bemorning shikoyatlari
    predicted_disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True)
    analysis_notes = models.TextField(blank=True, null=True)  # Tahlil natijalari haqida eslatmalar
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.age} years)"


class EKGAnalysis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='ekg_images')
    image = models.ImageField(upload_to='ekg_images/')
    analysis_data = models.JSONField(blank=True, null=True)  # Store extracted data
    diagnosis = models.CharField(max_length=255, blank=True, null=True)
    recommended_medicine = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
