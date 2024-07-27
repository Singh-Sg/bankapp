from django.urls import path
from .views import DepositAPIView, WithdrawalAPIView, MoneyTransferAPIView, StatementAPIView

urlpatterns = [
    path("api/deposit/<int:account_number>/", DepositAPIView.as_view(), name="deposit"),
    path(
        "api/withdrawal/<int:account_number>/", WithdrawalAPIView.as_view(), name="withdrawal"
    ),
    path("api/transfer/", MoneyTransferAPIView.as_view(), name="transfer"),
    path(
        "api/StatementAPIView/<int:account_number>/",
        StatementAPIView.as_view(),
        name="statement",
    ),
]
