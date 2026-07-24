from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from common.constants import LOGIN_SUCCESS,REGISTER_SUCCESS
from common.responses import ApiResponse

from .serializers import LoginSerializer
from .serializers import RegisterSerializer


class RegisterAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

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