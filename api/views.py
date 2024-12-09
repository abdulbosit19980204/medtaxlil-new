from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from .models import CustomUser
from users.serializers import LoginResponseSerializer
from django.utils.translation import activate, gettext as _
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema


class AuthUserView(RetrieveAPIView):
    """
    Token asosida foydalanuvchini olish
    Avtorizatsiyadan o'tgan foydalanuvchini olish uchun:
    """
    queryset = CustomUser.objects.all()
    serializer_class = LoginResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        print(self.request)
        return self.request.user


class SetLanguageAPIView(APIView):
    """
    API endpoint to set the user's language preference.
    """
    permission_classes = [IsAuthenticated]  # Optional: Require authentication if needed

    def get(self, request, *args, **kwargs):
        """
        Returns the available languages.
        """
        available_languages = getattr(settings, 'LANGUAGES', [])
        return Response(
            {"languages": [{"code": code, "name": str(name)} for code, name in available_languages]},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Set the user's language preference.",
        # request_body="language_code",
        responses={
            201: "Language setting successfully.",
            400: "Invaild language code."
        }
    )
    def post(self, request, *args, **kwargs):
        print(request.data)
        language_code = request.data.get('language_code')  # Expecting JSON payload with "language_code"
        if not language_code:
            return Response(
                {"detail": _("Language code is required.")},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Activate the language
        try:
            activate(language_code)
            request.session['django_language'] = language_code
            return Response(
                {"detail": _("Language has been set successfully."), "language_code": language_code},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"detail": _("Invalid language code."), "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
