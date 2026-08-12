from decimal import Decimal

import pytest

from accounts.models import Account
from accounts.services import AccountService
from transactions.models import Transaction


@pytest.mark.django_db
def test_statement_pdf_api_success(authenticated_client, account):

    account.balance = Decimal("1000.00")
    account.save()

    Transaction.objects.create(
        account=account,
        transaction_type=Transaction.TransactionType.DEPOSIT,
        amount=Decimal("500.00"),
        balance_after_transaction=Decimal("1000.00"),
    )

    response = authenticated_client.get(
        "/api/v1/transactions/statement/pdf/"
    )

    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"


@pytest.mark.django_db
def test_statement_pdf_api_requires_authentication(api_client):

    response = api_client.get(
        "/api/v1/transactions/statement/pdf/"
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_statement_csv_api_success(authenticated_client, account):

    account.balance = Decimal("1000.00")
    account.save()

    Transaction.objects.create(
        account=account,
        transaction_type=Transaction.TransactionType.DEPOSIT,
        amount=Decimal("500.00"),
        balance_after_transaction=Decimal("1000.00"),
    )

    response = authenticated_client.get(
        "/api/v1/transactions/statement/csv/"
    )

    assert response.status_code == 200
    assert "text/csv" in response["Content-Type"]


@pytest.mark.django_db
def test_statement_csv_api_requires_authentication(api_client):

    response = api_client.get(
        "/api/v1/transactions/statement/csv/"
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_statement_pdf_api_date_filter(
    authenticated_client,
    account,
):

    account.balance = Decimal("1000.00")
    account.save()

    Transaction.objects.create(
        account=account,
        transaction_type=Transaction.TransactionType.DEPOSIT,
        amount=Decimal("500.00"),
        balance_after_transaction=Decimal("1000.00"),
    )

    response = authenticated_client.get(
        "/api/v1/transactions/statement/pdf/",
        {
            "start_date": "2026-01-01",
            "end_date": "2026-12-31",
        },
    )

    assert response.status_code == 200
    assert response["Content-Type"] == "application/pdf"


@pytest.mark.django_db
def test_statement_csv_api_date_filter(
    authenticated_client,
    account,
):

    account.balance = Decimal("1000.00")
    account.save()

    Transaction.objects.create(
        account=account,
        transaction_type=Transaction.TransactionType.DEPOSIT,
        amount=Decimal("500.00"),
        balance_after_transaction=Decimal("1000.00"),
    )

    response = authenticated_client.get(
        "/api/v1/transactions/statement/csv/",
        {
            "start_date": "2026-01-01",
            "end_date": "2026-12-31",
        },
    )

    assert response.status_code == 200
    assert "text/csv" in response["Content-Type"]



@pytest.mark.django_db
def test_statement_api_invalid_date_range(authenticated_client):

    response = authenticated_client.get(
        "/api/v1/transactions/statement/pdf/",
        {
            "start_date": "2026-12-31",
            "end_date": "2026-01-01",
        },
    )

    assert response.status_code == 400