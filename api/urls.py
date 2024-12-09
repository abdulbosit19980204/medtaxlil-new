from django.urls import path
from .views import AuthUserView, SetLanguageAPIView
from patients.views import PatientView
from ekg.views import EKGImageView
from rest_framework.routers import DefaultRouter
from diseases.views import DiseaseViewSet, MedicationViewSet

urlpatterns = [
    path('user/', AuthUserView.as_view(), name='auth-user'),
    path('patients/', PatientView.as_view(), name='patients'),
    path('ekg-images/', EKGImageView.as_view(), name='ekg-images'),
    path('set-language/', SetLanguageAPIView.as_view(), name='set-language'),
]

router = DefaultRouter()
router.register(r'diseases', DiseaseViewSet, basename='disease')
router.register(r'medications', MedicationViewSet, basename='medication')

urlpatterns += router.urls
