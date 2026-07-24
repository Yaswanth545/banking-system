from rest_framework import permissions, status
from rest_framework.views import APIView

from common.responses import ApiResponse

from .serializers import DepositSerializer
from .services import TransactionService


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