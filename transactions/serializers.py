from decimal import Decimal

from rest_framework import serializers


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