from django.urls import path

from .views import CreateAccountAPIView, MyAccountAPIView,BeneficiaryCreateAPIView

urlpatterns = [
    path("", CreateAccountAPIView.as_view(), name="create-account"),
    path("me/",MyAccountAPIView.as_view(),name="my-account"),
    path("beneficiaries/",BeneficiaryCreateAPIView.as_view(),name="add-beneficiary",),
]