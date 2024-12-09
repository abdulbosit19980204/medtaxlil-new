from os import fpathconf
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from api.models import Patient, EKGAnalysis
from .serializers import EKGAnalysisSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from PIL import Image
import cv2
import numpy as np
from scipy.signal import find_peaks
from drf_yasg.utils import swagger_auto_schema
from api.custom_paginator import CustomPagination


class EKGImageView(ListCreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = EKGAnalysisSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination  # Custom Paginationni qo‘shamiz

    def extract_waveform(self, image_array):
        """Process the image to extract the waveform."""
        _, binary_image = cv2.threshold(image_array, 128, 255, cv2.THRESH_BINARY_INV)
        edges = cv2.Canny(binary_image, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        waveform = max(contours, key=cv2.contourArea)
        return waveform

    def analyze_waveform(self, waveform):
        """Analyze the extracted waveform."""
        signal = waveform[:, 0, 1]
        signal = (signal - np.min(signal)) / (np.max(signal) - np.min(signal))
        peaks, _ = find_peaks(signal, height=0.5, distance=30)
        if len(peaks) > 1:
            rr_intervals = np.diff(peaks)
            avg_rr_interval = np.mean(rr_intervals)
            heart_rate = 60 / avg_rr_interval
        else:
            heart_rate = None
        return signal, peaks, heart_rate

    def diagnose(self, heart_rate):
        """Provide diagnosis and medicine based on heart rate."""
        if heart_rate is None:
            return "Unable to detect heart rate", "Consult a cardiologist"
        elif heart_rate < 60:
            return "Bradycardia", "Beta-blockers"
        elif heart_rate > 100:
            return "Tachycardia", "Calcium channel blockers"
        else:
            return "Normal Heart Rhythm", "No medicine needed"

    @swagger_auto_schema(
        operation_description="Analyze an EKG image and provide diagnosis.",
        request_body=EKGAnalysisSerializer,
        responses={
            200: "EKG image analyzed successfully.",
            400: "Invalid EKG image."
        }
    )
    def post(self, request, *args, **kwargs):
        file = request.data.get('image')
        print("*" * 50, request.data.__dict__)
        patient_id = self.request.data.get('patient')

        patient = Patient.objects.get(id=patient_id, user=self.request.user)
        if not file:
            return Response({"error": "No image provided."}, status=400)

        analysis = EKGAnalysis.objects.create(image=file, patient=patient)
        try:
            image = Image.open(analysis.image.path).convert('L')
            image_array = np.array(image)
            waveform = self.extract_waveform(image_array)
            signal, peaks, heart_rate = self.analyze_waveform(waveform)
            diagnosis, medicine = self.diagnose(heart_rate)

            analysis.analysis_data = {
                "heart_rate": heart_rate,
                "peaks": peaks.tolist() if peaks is not None else None,
                "signal": signal.tolist(),
            }
            analysis.diagnosis = diagnosis
            analysis.recommended_medicine = medicine
            analysis.save()

        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response(EKGAnalysisSerializer(analysis).data)

    def get_queryset(self):
        return EKGAnalysis.objects.filter(patient__user=self.request.user)

    def perform_create(self, serializer):
        patient_id = self.request.data.get('patient')
        patient = Patient.objects.get(id=patient_id, user=self.request.user)
        serializer.save(patient=patient)
