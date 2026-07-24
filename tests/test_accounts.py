import pytest

from tests.base import BaseAPITest


@pytest.mark.django_db
class TestAccountAPI(BaseAPITest):

    def test_get_my_account(self, authenticated_client):

        response = authenticated_client.get(
            self.url("my-account")
        )

        assert response.status_code == 200

    def test_unauthenticated_user_cannot_access_account(self):

        response = self.client.get(
            self.url("my-account")
        )

        assert response.status_code == 401