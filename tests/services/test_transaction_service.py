import pytest
from decimal import Decimal

from common.business_exceptions import (
    InsufficientBalanceException,
    AccountFrozenException,
    BusinessException,
)

from accounts.models import Account
from transactions.services import TransactionService



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


