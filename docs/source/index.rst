.. EKG Analize documentation master file, created by
sphinx-quickstart on Mon Dec  9 06:12:52 2024.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive.

EKG Analize documentation
=========================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

Bemor Tahlili API
==================

Loyihaning maqsadi - bemorlarning EKG natijalarini tahlil qilib, kasalliklarni aniqlash va dorilarni tavsiya qilish. Ushbu API, bemorlar uchun shifokorlar tomonidan aniqlangan tashxislarga asoslanib, tavsiyalar beradi.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api_reference

API Reference
==================

User Registration API
-----------------------

**POST** `/api/register/`

Bu endpoint orqali foydalanuvchi tizimga ro‘yxatdan o‘tishi mumkin.

**Request body**:

- `username`: string, required
- `email`: string, required
- `password`: string, required

**Response**:

- 201: User registered successfully.
- 400: User already exists.

Login API
-----------------------

**POST** `/api/login/`

Bu endpoint orqali foydalanuvchi tizimga kirishi mumkin.

**Request body**:

- `username`: string, required
- `password`: string, required

**Response**:

- 200: JWT Token successfully generated.
- 400: Invalid credentials.


Get User by Token API
-----------------------

**GET** `/api/user/`

Bu endpoint orqali foydalanuvchi tizimga kirishi mumkin.

**Request body**:

- `token`: string, required


**Response**:

"root":{9 items
    -"id": 1
    -"username": "test1"
    -"email": ""
    -"first_name": ""
    -"last_name": ""
    -"gender": "male"
    -"image": "http://localhost:8000/media/users/pictures/default.jpg"
    -"access_token": "e*****8kqwc"
    -"refresh_token": "ey***CD7w"
}