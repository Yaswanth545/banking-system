from rest_framework import serializers

from .models import Account,Beneficiary


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


class BeneficiarySerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(write_only=True)

    class Meta:
        model = Beneficiary
        fields = (
            "account_number",
            "nickname",
        )

    def validate_account_number(self, value):
        try:
            Account.objects.get(account_number=value)
        except Account.DoesNotExist:
            raise serializers.ValidationError(
                "Account does not exist."
            )

        return value