from rest_framework import serializers

from .models import Account


class CreateAccountSerializer(serializers.Serializer):
    account_type = serializers.ChoiceField(
        choices=Account.AccountType.choices
    )