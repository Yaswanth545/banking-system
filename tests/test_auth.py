import pytest
from django.contrib.auth import get_user_model

from tests.base import BaseAPITest

User = get_user_model()


@pytest.mark.django_db
class TestRegisterAPI(BaseAPITest):

    def test_user_can_register(self,registration_payload):

       
        response = self.client.post(
            self.url("register"),
            registration_payload,
            format="json",
        )

        assert response.status_code == 201
        assert User.objects.filter(
            email="john@gmail.com"
        ).exists()



    def test_duplicate_email_registration(self,registration_payload):
        User.objects.create_user(
            email="john@gmail.com",
            username="john",
            phone_number="+919876543210",
            password="Password@123",
        )

        registration_payload["username"] = "john2"
        registration_payload["phone_number"] = "9876543211"

        response = self.client.post(
            self.url("register"),
            registration_payload,
            format="json",
        )

        assert response.status_code == 400

        assert "errors" in response.data
        assert "email" in response.data["errors"]



    def test_password_mismatch(self,registration_payload):

        registration_payload["confirm_password"] = "Password@456"
        
        response = self.client.post(
            self.url("register"),
            registration_payload,
            format="json",
        )

        assert response.status_code == 400

        assert "errors" in response.data
        assert "confirm_password" in response.data["errors"]


    def test_invalid_phone_number(self,registration_payload):

        registration_payload["phone_number"] = "123"
        
        response = self.client.post(
            self.url("register"),
            registration_payload,
            format="json",
        )

        assert response.status_code == 400

        assert "errors" in response.data
        assert "phone_number" in response.data["errors"]

    def test_username_is_required(self,registration_payload):
        
        registration_payload.pop("username")

        response = self.client.post(
            self.url("register"),
            registration_payload,
            format="json",
        )

        assert response.status_code == 400