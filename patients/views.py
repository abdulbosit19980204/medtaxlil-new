from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from api.models import Patient
from .serializers import PatientSerializer


class PatientView(ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
