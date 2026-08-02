from decimal import Decimal

from rest_framework import serializers
from .models import Transaction


class DepositSerializer(serializers.Serializer):

    amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    def validate_amount(self, value):

        if value <= Decimal("0.00"):
            raise serializers.ValidationError(
                "Deposit amount must be greater than zero."
            )

        return value
    



class WithdrawSerializer(serializers.Serializer):

    amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    def validate_amount(self, value):
        if value <= Decimal("0.00"):
            raise serializers.ValidationError(
                "Withdrawal amount must be greater than zero."
            )

        return value
    

class TransferSerializer(serializers.Serializer):

    receiver_account_number = serializers.CharField(
        max_length=20
    )

    amount = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    def validate_amount(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero."
            )

        return value
    

class TransactionHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            "id",
            "transaction_type",
            "amount",
            "balance_after_transaction",
            "created_at",
        )


class StatementSerializer(serializers.Serializer):
    """
    Validate query parameters for statement export.
    """

    start_date = serializers.DateField(
        required=False,
    )

    end_date = serializers.DateField(
        required=False,
    )

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                "start_date cannot be greater than end_date."
            )

        return attrs