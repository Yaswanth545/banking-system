from django.urls import path

from .views import CreateAccountAPIView, MyAccountAPIView

urlpatterns = [
    path("", CreateAccountAPIView.as_view(), name="create-account"),
    path("me/",MyAccountAPIView.as_view(),name="my-account"),
]