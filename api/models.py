from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    image = models.ImageField(upload_to='users/pictures/', default='/users/pictures/default.jpg')
    phone = models.CharField(max_length=11, blank=True, null=True)


class Patient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patients')
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    complaints = models.TextField()  # Bemorning shikoyatlari
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
