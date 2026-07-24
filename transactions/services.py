from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from common.business_exceptions import (
    InsufficientBalanceException,
    AccountFrozenException,
)

from accounts.models import Account
from .models import Transaction


class TransactionService:

    @staticmethod
    @transaction.atomic
    def deposit(user, amount):
        """
        Deposit money into the authenticated user's account.
        """

        account = (
            Account.objects
            .select_for_update()
            .get(user=user)
        )

        account.balance = F("balance") + amount
        account.save(update_fields=["balance"])

        account.refresh_from_db()

        Transaction.objects.create(
            account=account,
            transaction_type=Transaction.TransactionType.DEPOSIT,
            amount=amount,
            balance_after_transaction=account.balance,
        )

        return account
    
    
    
    @staticmethod
    @transaction.atomic
    def withdraw(user, amount):

        account = (
            Account.objects
            .select_for_update()
            .get(user=user)
        )

        if account.status != Account.AccountStatus.ACTIVE:
            raise AccountFrozenException()

        if account.balance < amount:
            raise InsufficientBalanceException()

        account.balance = F("balance") - amount
        account.save(update_fields=["balance"])

        account.refresh_from_db()

        Transaction.objects.create(
            account=account,
            transaction_type=Transaction.TransactionType.WITHDRAW,
            amount=amount,
            balance_after_transaction=account.balance,
        )

        return account
    
    @staticmethod
    def _lock_accounts(sender, receiver):

        account_ids = sorted([
            sender.id,
            receiver.id,
        ])

        accounts = (
            Account.objects
            .select_for_update()
            .filter(id__in=account_ids)
            .order_by("id")
        )

        return {
            account.id: account
            for account in accounts
        }
        



    