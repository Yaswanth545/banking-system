import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from accounts.models import Account

User = get_user_model()


@pytest.fixture
def registration_payload():
    return {
        "email": "john@gmail.com",
        "username": "john",
        "phone_number": "9876543210",
        "password": "Password@123",
        "confirm_password": "Password@123",
    }


@pytest.fixture
def user():
    return User.objects.create_user(
        email="john@gmail.com",
        username="john",
        phone_number="+919876543210",
        password="Password@123",
    )


@pytest.fixture
def account(user):
    return Account.objects.get(user=user)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user, account):
    api_client.force_authenticate(user=user)
    return api_client