from django.urls import path

from .views import DepositAPIView

urlpatterns = [
    path("deposit/",DepositAPIView.as_view(),name="deposit"),
]