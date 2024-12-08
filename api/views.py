from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from .models import CustomUser
from users.serializers import LoginResponseSerializer


class AuthUserView(RetrieveAPIView):
    """
    Token asosida foydalanuvchini olish
    Avtorizatsiyadan o'tgan foydalanuvchini olish uchun:
    """
    queryset = CustomUser.objects.all()
    serializer_class = LoginResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
