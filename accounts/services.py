from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Account
from .utils import generate_account_number


class AccountService:

    @staticmethod
    @transaction.atomic
    def create_account(user, account_type):

        if Account.objects.filter(user=user).exists():
            raise ValidationError(
                "User already has a bank account."
            )

        account = Account.objects.create(
            user=user,
            account_number=generate_account_number(),
            account_type=account_type,
        )

        return account