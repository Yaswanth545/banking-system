import pytest
from decimal import Decimal

from accounts.models import Account
from transactions.models import Transaction
from common.business_exceptions import InsufficientBalanceException
from accounts.services import AccountService



@pytest.mark.django_db
def test_deposit_api_success(authenticated_client, account):

    response = authenticated_client.post(
        "/api/v1/transactions/deposit/",
        {
            "amount": "500.00",
        },
        format="json",
    )

    assert response.status_code == 200

    account.refresh_from_db()

    assert account.balance == Decimal("10500.00")

    assert Transaction.objects.filter(
        account=account,
        transaction_type=Transaction.TransactionType.DEPOSIT,
        amount=Decimal("500.00"),
    ).exists()


@pytest.mark.django_db
def test_deposit_api_invalid_amount(authenticated_client):

    response = authenticated_client.post(
        "/api/v1/transactions/deposit/",
        {
            "amount": "0",
        },
        format="json",
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_deposit_api_requires_authentication(api_client):

    response = api_client.post(
        "/api/v1/transactions/deposit/",
        {
            "amount": "500.00",
        },
        format="json",
    )

    assert response.status_code == 401



@pytest.mark.django_db
def test_withdraw_api_success(authenticated_client, account):

    account.balance = Decimal("1000.00")
    account.save()

    response = authenticated_client.post(
        "/api/v1/transactions/withdraw/",
        {
            "amount": "300.00",
        },
        format="json",
    )

    assert response.status_code == 200

    account.refresh_from_db()

    assert account.balance == Decimal("700.00")



@pytest.mark.django_db
def test_withdraw_api_insufficient_balance(
    authenticated_client,
    account,
):

    account.balance = Decimal("100.00")
    account.save()

    response = authenticated_client.post(
        "/api/v1/transactions/withdraw/",
        {
            "amount": "500.00",
        },
        format="json",
    )

    assert response.status_code == 400

    account.refresh_from_db()

    assert account.balance == Decimal("100.00")



@pytest.mark.django_db
def test_withdraw_api_requires_authentication(api_client):

    response = api_client.post(
        "/api/v1/transactions/withdraw/",
        {
            "amount": "300.00",
        },
        format="json",
    )

    assert response.status_code == 401



@pytest.mark.django_db
def test_transfer_api_success(authenticated_client, account, user):

    receiver_user = type(user).objects.create_user(
        email="receiver@gmail.com",
        username="receiver",
        phone_number="+919876543211",
        password="Password@123",
    )

    receiver_account = AccountService.create_account(
    user=receiver_user,
    account_type=Account.AccountType.SAVINGS,
)

    receiver_account.balance = Decimal("500.00")
    receiver_account.save()

    account.balance = Decimal("1000.00")
    account.save()

    response = authenticated_client.post(
        "/api/v1/transactions/transfer/",
        {
            "receiver_account_number": receiver_account.account_number,
            "amount": "300.00",
        },
        format="json",
    )

    
    assert response.status_code == 200

    account.refresh_from_db()
    receiver_account.refresh_from_db()

    assert account.balance == Decimal("700.00")
    assert receiver_account.balance == Decimal("800.00")


@pytest.mark.django_db
def test_transfer_api_insufficient_balance(
    authenticated_client,
    account,
    user,
):

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

    response = authenticated_client.post(
        "/api/v1/transactions/transfer/",
        {
            "receiver_account_number": receiver_account.account_number,
            "amount": "500.00",
        },
        format="json",
    )

    assert response.status_code == 400

    account.refresh_from_db()
    receiver_account.refresh_from_db()

    assert account.balance == Decimal("100.00")
    assert receiver_account.balance == Decimal("500.00")


@pytest.mark.django_db
def test_transfer_api_same_account(
    authenticated_client,
    account,
):

    account.balance = Decimal("1000.00")
    account.save()

    response = authenticated_client.post(
        "/api/v1/transactions/transfer/",
        {
            "receiver_account_number": account.account_number,
            "amount": "300.00",
        },
        format="json",
    )

    assert response.status_code == 400

    account.refresh_from_db()

    assert account.balance == Decimal("1000.00")



@pytest.mark.django_db
def test_transfer_api_requires_authentication(
    api_client,
    account,
):

    response = api_client.post(
        "/api/v1/transactions/transfer/",
        {
            "receiver_account_number": account.account_number,
            "amount": "300.00",
        },
        format="json",
    )

    assert response.status_code == 401