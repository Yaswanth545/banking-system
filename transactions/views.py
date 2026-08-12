from rest_framework import permissions, status,generics
from rest_framework.views import APIView
from rest_framework.response import Response


from common.responses import ApiResponse

from .models import Transaction
from .serializers import DepositSerializer,WithdrawSerializer,TransferSerializer,TransactionHistorySerializer,StatementSerializer
from .services import TransactionService
from common.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend

from .filters import TransactionFilter
from drf_spectacular.utils import (extend_schema,OpenApiExample,OpenApiResponse,)

from django.http import HttpResponse,FileResponse
from .statement_service import StatementService
from .cache_service import CacheService




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
            .select_related("account")
            .filter(account__user=self.request.user)
            .order_by("-created_at")
        )
    
    def list(self, request, *args, **kwargs):
        cached_response = CacheService.get_transaction_history(
            request.user.id
        )

        if cached_response:
            return Response(cached_response)
        
        response = super().list(
            request,
            *args,
            **kwargs,
        )


        CacheService.set_transaction_history(request.user.id,response.data,)

        return response


class StatementPDFAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        serializer = StatementSerializer(
            data=request.query_params
        )

        serializer.is_valid(
            raise_exception=True
        )

        pdf = StatementService.generate_pdf(
            user=request.user,
            start_date=serializer.validated_data.get("start_date"),
            end_date=serializer.validated_data.get("end_date"),
        )

        return FileResponse(
            pdf,
            as_attachment=True,
            filename="account_statement.pdf",
            content_type="application/pdf",
        )
    


class StatementCSVAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        serializer = StatementSerializer(
            data=request.query_params
        )

        serializer.is_valid(
            raise_exception=True
        )

        csv_buffer = StatementService.generate_csv(
            user=request.user,
            start_date=serializer.validated_data.get("start_date"),
            end_date=serializer.validated_data.get("end_date"),
        )

        response = HttpResponse(
            csv_buffer.getvalue(),
            content_type="text/csv",
        )

        response["Content-Disposition"] = (
            'attachment; filename="account_statement.csv"'
        )

        return response