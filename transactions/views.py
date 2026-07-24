from rest_framework import permissions, status,generics
from rest_framework.views import APIView

from common.responses import ApiResponse

from .models import Transaction
from .serializers import DepositSerializer,WithdrawSerializer,TransferSerializer,TransactionHistorySerializer
from .services import TransactionService
from common.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend

from .filters import TransactionFilter
from drf_spectacular.utils import (extend_schema,OpenApiExample,OpenApiResponse,)



@extend_schema(
    summary="Deposit Money",
    description="Deposit money into the authenticated user's account.",
    request=DepositSerializer,
    responses={
        200: OpenApiResponse(description="Deposit completed successfully."),
        400: OpenApiResponse(description="Validation failed."),
    },
    tags=["Transactions"],
)
class DepositAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = TransactionService.deposit(
            user=request.user,
            amount=serializer.validated_data["amount"],
        )

        return ApiResponse.success(
            message="Amount deposited successfully.",
            data={
                "balance": str(account.balance),
            },
            status_code=status.HTTP_200_OK,
        )
    




@extend_schema(
    summary="Withdraw Money",
    description="Withdraw money from the authenticated user's account.",
    request=WithdrawSerializer,
    responses={
        200: OpenApiResponse(description="Withdrawal completed successfully."),
        400: OpenApiResponse(description="Insufficient balance or validation failed."),
    },
    tags=["Transactions"],
)
class WithdrawAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        serializer = WithdrawSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = TransactionService.withdraw(
            user=request.user,
            amount=serializer.validated_data["amount"],
        )

        return ApiResponse.success(
            message="Amount withdrawn successfully.",
            data={
                "balance": str(account.balance),
            },
            status_code=status.HTTP_200_OK,
        )
    




@extend_schema(
    summary="Transfer Money",
    description="Transfer money from the authenticated user's account to another account.",
    request=TransferSerializer,
    responses={
        200: OpenApiResponse(description="Transfer completed successfully."),
        400: OpenApiResponse(description="Transfer failed."),
    },
    tags=["Transactions"],
)
class TransferAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transfer = TransactionService.transfer(
            sender_user=request.user,
            receiver_account_number=serializer.validated_data[
                "receiver_account_number"
            ],
            amount=serializer.validated_data["amount"],
        )

        return ApiResponse.success(
            message="Money transferred successfully.",
            data={
                "reference_number": str(transfer.reference_number),
            },
            status_code=status.HTTP_200_OK,
        )
    
@extend_schema(
    summary="Transaction History",
    description="Retrieve paginated transaction history for the authenticated user.",
    responses={
        200: OpenApiResponse(description="Transaction history retrieved successfully."),
    },
    tags=["Transactions"],
)
class TransactionHistoryAPIView(generics.ListAPIView):
    """
    Retrieve transaction history for the authenticated user.
    """

    serializer_class = TransactionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter


    def get_queryset(self):
        return (
            Transaction.objects
            .filter(account__user=self.request.user)
            .order_by("-created_at")
        )