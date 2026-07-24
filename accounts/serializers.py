from rest_framework import serializers

from .models import Account


class CreateAccountSerializer(serializers.Serializer):
    account_type = serializers.ChoiceField(
        choices=Account.AccountType.choices
    )


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = (
            "account_number",
            "account_type",
            "balance",
            "currency",
            "status",
            "created_at",
        )