from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from common.constants import LOGIN_SUCCESS,REGISTER_SUCCESS
from common.responses import ApiResponse

from .serializers import LoginSerializer
from .serializers import RegisterSerializer

from drf_spectacular.utils import (extend_schema,OpenApiExample,OpenApiResponse,)
from transactions.tasks import send_welcome_email


import logging
logger = logging.getLogger(__name__)



@extend_schema(
    summary="Register a new customer",
    description="Creates a new customer account in the banking system.",
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(description="Registration successful."),
        400: OpenApiResponse(description="Validation failed."),
    },
    tags=["Authentication"],
)
class RegisterAPIView(APIView):
    permission_classes = []

    def post(self, request):
        
        logger.info("Register API called")

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        send_welcome_email.delay(user.id)

        return ApiResponse.success(
            message=REGISTER_SUCCESS,
            data={
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "phone_number": user.phone_number,
                "role": user.role,
            },
            status_code=status.HTTP_201_CREATED,
        )




@extend_schema(
    summary="Login",
    description="Authenticate the user and return JWT access and refresh tokens.",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(description="Login successful."),
        401: OpenApiResponse(description="Invalid credentials."),
    },
    tags=["Authentication"],
)
class LoginAPIView(APIView):

    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return ApiResponse.success(
            message=LOGIN_SUCCESS,
            data={
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "role": user.role,
                },
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            },
        )