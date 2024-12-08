# users/utils.py
import difflib
from api.models import Disease



def analyze_complaint(complaint_text):
    # Kasalliklar va ularning simptomlarini olish
    diseases = Disease.objects.all()
    best_match = None
    highest_ratio = 0

    for disease in diseases:
        # Difflib yordamida simptomlar mosligini aniqlash
        match_ratio = difflib.SequenceMatcher(None, complaint_text.lower(), disease.symptoms.lower()).ratio()
        if match_ratio > highest_ratio:
            highest_ratio = match_ratio
            best_match = disease

    # Agar moslik 0.5 dan yuqori bo'lsa, mos kasallikni qaytaramiz
    if highest_ratio >= 0.5:
        return best_match, f"Match ratio: {highest_ratio:.2f}"
    return None, "No significant match found."
