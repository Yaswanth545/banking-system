from django.urls import reverse
from rest_framework.test import APIClient


class BaseAPITest:
    """
    Base class for API tests.
    """

    def setup_method(self):
        self.client = APIClient()

    def url(self, name, **kwargs):
        return reverse(name, kwargs=kwargs)