# ECG Analysis and Medication Recommendation System

![ECG Logo](https://img.shields.io/badge/Django%20REST-Backend-green)
![OpenCV](https://img.shields.io/badge/OpenCV-Image%20Processing-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 🔍 Overview

**ecg.med-taxlil.uz** — bu EKG (elektrokardiogramma) tasvirlarini avtomatik tahlil qiluvchi va aniqlangan yurak kasalliklariga asoslangan dori-darmon tavsiyalarini beruvchi tibbiy veb-platforma. Loyihada signal va tasvirlarni qayta ishlash, shuningdek mashinaviy o‘rganish usullari qo‘llanilgan.

## 🛠 Texnologiyalar

- **Backend:** Django Rest Framework (DRF)
- **Tasvir/signal ishlov berish:** OpenCV, Neurokit2
- **ML:** Scikit-learn, NumPy, Pandas
- **Ma'lumotlar bazasi:** PostgreSQL
- **Autentifikatsiya:** JWT
- **(Ixtiyoriy) Deploy:** Docker, Nginx, Gunicorn

## ✨ Asosiy funksiyalar

- ✅ Ro‘yxatdan o‘tish va login
- ✅ Bemor ma'lumotlarini kiritish
- ✅ EKG tasvir yuklash va tahlil qilish
- ✅ Signal xususiyatlarini ajratib olish
- ✅ ML yordamida kasallikni aniqlash
- ✅ Tavsiya etilgan dorilar ro‘yxatini taqdim etish
- ✅ Admin panel orqali kasallik va dori bazasini boshqarish
- ✅ RESTful API interfeysi
- ✅ Foydalanuvchilar uchun xavfsiz va rolli tizim


## 📁 Loyiha strukturasi

```text
ecg-med-taxlil/
├── api/                # Django ilovasi: views, models, serializers
├── media/              # Yuklangan EKG tasvirlari
├── ml/                 # ML modellar va signal tahlili
├── static/             # Statik fayllar
├── templates/          # Admin va boshqa HTML shablonlar
├── manage.py
└── requirements.txt
```

🚀 O‘rnatish (Local server uchun)
Repositoriyani klonlang:


git clone https://github.com/abdulbosit19980204/medtaxlil-new.git
cd ecg.med-taxlil.uz

-**Virtual muhit yarating va faollashtiring:**

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

-**Kerakli kutubxonalarni o‘rnating:**

pip install -r requirements.txt

-**PostgreSQL sozlamalarini .env yoki settings.py faylida kiriting.**

-**Migratsiyalarni bajaring va serverni ishga tushiring:**

python manage.py migrate
python manage.py runserver


⚙️ Admin Panel
Admin panel orqali quyidagilarni boshqarish mumkin:

Kasalliklar ro‘yxati

Dorilar bazasi

Bemorlar va foydalanuvchilar
