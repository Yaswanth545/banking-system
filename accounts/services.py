from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Account
from .utils import generate_account_number
from django.shortcuts import get_object_or_404




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
    
    @staticmethod
    def get_account(user):
        return get_object_or_404(
            Account,
            user=user
        )

