from django.urls import path

from .views import DepositAPIView,WithdrawAPIView,TransferAPIView,TransactionHistoryAPIView,StatementCSVAPIView,StatementPDFAPIView

urlpatterns = [
    path("",TransactionHistoryAPIView.as_view(),name="transaction-history",),
    path("deposit/",DepositAPIView.as_view(),name="deposit"),
    path("withdraw/",WithdrawAPIView.as_view(),name="withdraw",),
    path("transfer/",TransferAPIView.as_view(),name="transfer",),
    path("statement/pdf/",StatementPDFAPIView.as_view(),name="statement-pdf",),
    path("statement/csv/",StatementCSVAPIView.as_view(),name="statement-csv",),
]