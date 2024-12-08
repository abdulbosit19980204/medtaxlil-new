from django.urls import path
from .views import AuthUserView
from patients.views import PatientView
from ekg.views import EKGImageView

urlpatterns = [
    path('user/', AuthUserView.as_view(), name='auth-user'),
    path('patients/', PatientView.as_view(), name='patients'),
    path('ekg-images/', EKGImageView.as_view(), name='ekg-images'),
]
