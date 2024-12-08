from django.contrib import admin
from .models import EKGAnalysis, Patient, CustomUser

admin.site.register(EKGAnalysis)
admin.site.register(CustomUser)
admin.site.register(Patient)
