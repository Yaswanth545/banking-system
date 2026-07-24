from django.urls import path

from .views import DepositAPIView,WithdrawAPIView

urlpatterns = [
    path("deposit/",DepositAPIView.as_view(),name="deposit"),
    path("withdraw/",WithdrawAPIView.as_view(),name="withdraw",
),
]