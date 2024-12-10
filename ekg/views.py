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
        """Обработка изображения для извлечения формы сигнала."""
        _, binary_image = cv2.threshold(image_array, 128, 255, cv2.THRESH_BINARY_INV)
        edges = cv2.Canny(binary_image, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        waveform = max(contours, key=cv2.contourArea)
        return waveform

    def analyze_waveform(self, waveform):
        """Анализ извлеченной формы сигнала."""
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
        """Предоставить диагноз и рекомендации по лечению на основе частоты сердечных сокращений (ЧСС)."""
        if heart_rate is None:
            return "Невозможно определить ЧСС", "Проконсультируйтесь с кардиологом"
        elif heart_rate < 30:
            return "Жизнеугрожающая брадикардия", "Экстренное вмешательство (например, атропин, кардиостимуляция)"
        elif 30 <= heart_rate < 40:
            return "Тяжелая брадикардия", "Неотложная медицинская помощь"
        elif 40 <= heart_rate < 50:
            return "Умеренная брадикардия", "Консультация кардиолога для оценки состояния"
        elif 50 <= heart_rate < 60:
            return "Легкая брадикардия", "Возможен прием бета-блокаторов или наблюдение"
        elif 60 <= heart_rate <= 100:
            return "Нормальный ритм сердца", "Медикаментозное лечение не требуется"
        elif 101 <= heart_rate <= 110:
            return "Повышенная ЧСС", "Контроль и снижение стресса"
        elif 111 <= heart_rate <= 130:
            return "Легкая тахикардия", "Изменения образа жизни и наблюдение"
        elif 131 <= heart_rate <= 150:
            return "Умеренная тахикардия", "Антагонисты кальция или бета-блокаторы"
        elif 151 <= heart_rate <= 170:
            return "Тяжелая тахикардия", "Антиаритмические препараты и тщательное наблюдение"
        elif 171 <= heart_rate <= 190:
            return "Фибрилляция предсердий с быстрым желудочковым ответом", "Консультация кардиолога для контроля частоты"
        elif 191 <= heart_rate <= 220:
            return "Желудочковая тахикардия", "Неотложная медицинская помощь"
        elif heart_rate > 220:
            return "Критическое состояние", "Немедленное медицинское вмешательство"
        else:
            return "Неопознанный паттерн", "Консультация специалиста для дальнейшей оценки"

    @swagger_auto_schema(
        operation_description="Анализ ЭКГ изображения и предоставление диагноза.",
        request_body=EKGAnalysisSerializer,
        responses={
            200: "ЭКГ изображение успешно проанализировано.",
            400: "Недопустимое ЭКГ изображение."
        }
    )
    def post(self, request, *args, **kwargs):
        # print("*" * 50, request.__dict__)
        file = request.data.get('image')
        patient_id = self.request.data.get('patient')

        patient = Patient.objects.filter(id=patient_id, user=self.request.user).first()
        if not file:
            return Response({"error": "Изображение не предоставлено."}, status=400)
        elif not patient:
            return Response({"error": "Пациент не найден."}, status=400)
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
