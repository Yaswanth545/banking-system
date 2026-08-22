from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone

from transactions.models import Transaction


@pytest.mark.django_db
def test_transaction_history_api_success(
    authenticated_client,
    account,
):

    Transaction.objects.create(
        account=account,
        transaction_type=Transaction.TransactionType.DEPOSIT,
        amount=Decimal("500.00"),
        balance_after_transaction=Decimal("500.00"),
    )

    response = authenticated_client.get(
        "/api/v1/transactions/"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_transaction_history_api_requires_authentication(
    api_client,
):

    response = api_client.get(
        "/api/v1/transactions/"
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_transaction_history_api_pagination(
    authenticated_client,
    account,
):

    for amount in range(1, 6):
        Transaction.objects.create(
            account=account,
            transaction_type=Transaction.TransactionType.DEPOSIT,
            amount=Decimal(amount),
            balance_after_transaction=Decimal(amount),
        )

    response = authenticated_client.get(
        "/api/v1/transactions/?page=1&page_size=2"
    )

    assert response.status_code == 200
    assert response.data["count"] == 5
    assert len(response.data["results"]) == 2

@pytest.mark.django_db
def test_transaction_history_api_created_after_filter(
    authenticated_client,
    account,
):

    Transaction.objects.create(
        account=account,
        transaction_type=Transaction.TransactionType.DEPOSIT,
        amount=Decimal("100.00"),
        balance_after_transaction=Decimal("100.00"),
    )

    future_date = (
        timezone.now().date() + timedelta(days=1)
    )

    response = authenticated_client.get(
        "/api/v1/transactions/",
        {
            "start_date": future_date,
        },
    )

    assert response.status_code == 200
    assert response.data["count"] == 0


@pytest.mark.django_db
def test_transaction_history_api_created_before_filter(
    authenticated_client,
    account,
):

    Transaction.objects.create(
        account=account,
        transaction_type=Transaction.TransactionType.DEPOSIT,
        amount=Decimal("100.00"),
        balance_after_transaction=Decimal("100.00"),
    )

    future_date = (
        timezone.now().date() + timedelta(days=1)
    )

    response = authenticated_client.get(
        "/api/v1/transactions/",
        {
            "end_date": future_date,
        },
    )

    assert response.status_code == 200
    assert response.data["count"] == 1