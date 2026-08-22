import pytest
from decimal import Decimal

from common.business_exceptions import (
    InsufficientBalanceException,
    AccountFrozenException,
    BusinessException,
)

from accounts.models import Account
from transactions.services import TransactionService
from transactions.models import Transaction




@pytest.mark.django_db
def test_deposit_increases_balance(user, account):

    account.balance = Decimal("1000.00")
    account.save()

    TransactionService.deposit(
        user=user,
        amount=Decimal("500.00"),
    )

    account.refresh_from_db()

    assert account.balance == Decimal("1500.00")


@pytest.mark.django_db
def test_withdraw_decreases_balance(user, account):

    account.balance = Decimal("1000.00")
    account.save()

    TransactionService.withdraw(
        user=user,
        amount=Decimal("300.00"),
    )

    account.refresh_from_db()

    assert account.balance == Decimal("700.00")


@pytest.mark.django_db
def test_withdraw_with_insufficient_balance(account, user):
    account.balance = Decimal("100.00")
    account.save()

    initial_transaction_count = Transaction.objects.count()

    with pytest.raises(InsufficientBalanceException):
        TransactionService.withdraw(
            user=user,
            amount=Decimal("500.00"),
        )

    account.refresh_from_db()

    assert account.balance == Decimal("100.00")
    assert Transaction.objects.count() == initial_transaction_count



@pytest.mark.django_db
def test_withdraw_from_frozen_account(account, user):
    account.balance = Decimal("1000.00")
    account.status = Account.AccountStatus.FROZEN
    account.save()

    with pytest.raises(AccountFrozenException):
        TransactionService.withdraw(
            user=user,
            amount=Decimal("100.00"),
        )

    account.refresh_from_db()

    assert account.balance == Decimal("1000.00")