# users/utils.py
import difflib
from api.models import Disease


def analyze_complaint(complaint_text):
    """
    Ushbu funksiya foydalanuvchi shikoyatini jadvalda mavjud kasalliklar bilan moslashtiradi.
    U 'Symptoms' va 'Description' maydonlarini uch tilda tekshiradi.
    """
    diseases = Disease.objects.all()
    best_match = None
    highest_ratio = 0

    # Foydalanuvchi matnini kichik harflarga o'girish
    complaint_text = complaint_text.lower()

    for disease in diseases:
        # 'Symptoms' maydoni tilda ajratilganligini hisobga olish
        symptoms_text = f"{disease.symptoms}".lower()
        description_text = f"{disease.description}".lower()

        # Shikoyat matnini 'Symptoms' va 'Description' bilan solishtirish
        symptoms_ratio = difflib.SequenceMatcher(None, complaint_text, symptoms_text).ratio()
        description_ratio = difflib.SequenceMatcher(None, complaint_text, description_text).ratio()

        # Yuqori moslikni aniqlash (Symptoms yoki Description bo'yicha)
        max_ratio = max(symptoms_ratio, description_ratio)

        if max_ratio > highest_ratio:
            highest_ratio = max_ratio
            best_match = disease

    # Agar moslik 0.5 dan yuqori bo'lsa, mos kasallikni qaytaradi
    if highest_ratio >= 0.5:
        return best_match, f"Match ratio: {highest_ratio:.2f}    name: {best_match.name}, symptoms: {best_match.symptoms}"
    return None, "No significant match found."
