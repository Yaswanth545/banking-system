from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import permissions, status
from rest_framework.views import APIView

from common.responses import ApiResponse

from .serializers import CreateAccountSerializer,AccountSerializer,BeneficiarySerializer
from .services import AccountService,BeneficiaryService


class CreateAccountAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        serializer = CreateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            account = AccountService.create_account(
                user=request.user,
                account_type=serializer.validated_data["account_type"],
            )

        except DjangoValidationError as exc:
            return ApiResponse.error(
                message=str(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return ApiResponse.success(
            message="Account created successfully.",
            data={
                "account_number": account.account_number,
                "account_type": account.account_type,
                "balance": str(account.balance),
                "currency": account.currency,
                "status": account.status,
            },
            status_code=status.HTTP_201_CREATED,
        )
    

class MyAccountAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        account = AccountService.get_account(request.user)

        serializer = AccountSerializer(account)

        return ApiResponse.success(
            message="Account fetched successfully.",
            data=serializer.data,
        )
    


class BeneficiaryCreateAPIView(APIView):
    """
    Add a beneficiary for the authenticated user.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = BeneficiarySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        beneficiary = BeneficiaryService.add_beneficiary(
            owner=request.user,
            account_number=serializer.validated_data["account_number"],
            nickname=serializer.validated_data["nickname"],
        )

        return ApiResponse.success(
            message="Beneficiary added successfully.",
            data={
                "id": beneficiary.id,
                "nickname": beneficiary.nickname,
            },
            status_code=status.HTTP_201_CREATED,
        )