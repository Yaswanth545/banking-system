import pytest
from decimal import Decimal

from transactions.services import TransactionService
from transactions.models import Transfer
from common.business_exceptions import (
    InsufficientBalanceException,
    AccountFrozenException,
    ReceiverAccountInactiveException,
    BusinessException,
)

from accounts.models import Account


@pytest.mark.django_db
def test_transfer_success(user, account):
    receiver_user = type(user).objects.create_user(
        email="receiver@gmail.com",
        username="receiver",
        phone_number="+919876543211",
        password="Password@123",
    )

    

    receiver_account = Account.objects.create(
        user=receiver_user,
        balance=Decimal("500.00"),
    )

    account.balance = Decimal("1000.00")
    account.save()

    transfer = TransactionService.transfer(
        sender_user=user,
        receiver_account_number=receiver_account.account_number,
        amount=Decimal("300.00"),
    )

    account.refresh_from_db()
    receiver_account.refresh_from_db()

    assert transfer.status == "SUCCESS"
    assert account.balance == Decimal("700.00")
    assert receiver_account.balance == Decimal("800.00")


@pytest.mark.django_db
def test_transfer_insufficient_balance(user, account):
    receiver_user = type(user).objects.create_user(
        email="receiver@gmail.com",
        username="receiver",
        phone_number="+919876543211",
        password="Password@123",
    )


    receiver_account = Account.objects.create(
        user=receiver_user,
        balance=Decimal("500.00"),
    )

    account.balance = Decimal("100.00")
    account.save()

    with pytest.raises(InsufficientBalanceException):
        TransactionService.transfer(
            sender_user=user,
            receiver_account_number=receiver_account.account_number,
            amount=Decimal("500.00"),
        )

    account.refresh_from_db()
    receiver_account.refresh_from_db()

    assert account.balance == Decimal("100.00")
    assert receiver_account.balance == Decimal("500.00")


@pytest.mark.django_db
def test_transfer_to_same_account(user, account):
    with pytest.raises(BusinessException):
        TransactionService.transfer(
            sender_user=user,
            receiver_account_number=account.account_number,
            amount=Decimal("100.00"),
        )


@pytest.mark.django_db
def test_transfer_from_frozen_account(user, account):
    from accounts.models import Account

    receiver_user = type(user).objects.create_user(
        email="receiver@gmail.com",
        username="receiver",
        phone_number="+919876543211",
        password="Password@123",
    )

    receiver_account = Account.objects.create(
        user=receiver_user,
        balance=Decimal("500.00"),
    )

    account.status = Account.AccountStatus.FROZEN
    account.balance = Decimal("1000.00")
    account.save()

    with pytest.raises(AccountFrozenException):
        TransactionService.transfer(
            sender_user=user,
            receiver_account_number=receiver_account.account_number,
            amount=Decimal("100.00"),
        )


@pytest.mark.django_db
def test_transfer_to_inactive_account(user, account):
    from accounts.models import Account

    receiver_user = type(user).objects.create_user(
        email="receiver@gmail.com",
        username="receiver",
        phone_number="+919876543211",
        password="Password@123",
    )

    receiver_account = Account.objects.create(
        user=receiver_user,
        balance=Decimal("500.00"),
        status=Account.AccountStatus.FROZEN,
    )

    account.balance = Decimal("1000.00")
    account.save()

    with pytest.raises(ReceiverAccountInactiveException):
        TransactionService.transfer(
            sender_user=user,
            receiver_account_number=receiver_account.account_number,
            amount=Decimal("100.00"),
        )