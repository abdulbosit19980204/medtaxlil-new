from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from api.models import Patient, EKGAnalysis
from .serializers import PatientSerializer
from .utils import analyze_complaint
from .serializers import PrescriptionSerializer
from rest_framework.views import APIView


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
        phone = data['phone']
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
            phone=phone,
        )

        serializer = PatientSerializer(complaint)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PrescriptionView(APIView):
    """
    API endpoint to fetch the prescription for a patient based on their ID.
    """
    permission_classes = [IsAuthenticated]  # Optional: Require authentication if needed

    def get(self, request, patient_id, *args, **kwargs):
        try:
            # Fetch the patient by ID
            patient = Patient.objects.get(id=patient_id)

            # Fetch the latest EKGAnalysis for the patient
            ekg_analysis = EKGAnalysis.objects.filter(patient=patient).latest('uploaded_at')

            # Serialize the EKGAnalysis data
            serializer = PrescriptionSerializer(ekg_analysis)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response(
                {"detail": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except EKGAnalysis.DoesNotExist:
            return Response(
                {"detail": "No EKG Analysis found for this patient."},
                status=status.HTTP_404_NOT_FOUND
            )
