from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.models import Patient
from .serializers import PatientSerializer
from .utils import analyze_complaint


class PatientView(ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request):
        data = request.data
        complaints = request.data.get('complaints', '')
        full_name = request.data.get('full_name', '')
        age = data['age']
        gender = request.data.get('gender', '')
        if not complaints:
            return Response({"error": "Shikoyat matni kerak."}, status=status.HTTP_400_BAD_REQUEST)

        # Shikoyatni tahlil qilish
        predicted_disease, analysis_notes = analyze_complaint(complaints)

        # Natijalarni saqlash
        complaint = Patient.objects.create(
            complaints=complaints,
            predicted_disease=predicted_disease,
            analysis_notes=analysis_notes,
            full_name=full_name,
            age=age,
            gender=gender,
            user=self.request.user,
        )

        serializer = PatientSerializer(complaint)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
