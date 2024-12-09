# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginResponseSerializer
from drf_yasg.utils import swagger_auto_schema


class RegisterView(APIView):
    """
       User Registration API endpoint.

       **POST** `/api/register/`

       - `username`: string, required
       - `email`: string, required
       - `password`: string, required

       Response:
       - 201: User registered successfully.
       - 400: User already exists.
       """

    @swagger_auto_schema(
        operation_description="User registration endpoint.",
        request_body=RegisterSerializer,
        responses={
            201: "User registered successfully.",
            400: "User already exists."
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="User login endpoint.",
        request_body=LoginResponseSerializer,
        responses={
            200: "JWT Token successfully generated.",
            400: "Invalid credentials."
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            serializer = LoginResponseSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
