from django.urls import path

from .views import CreateAccountAPIView

urlpatterns = [
    path("", CreateAccountAPIView.as_view(), name="create-account"),
]