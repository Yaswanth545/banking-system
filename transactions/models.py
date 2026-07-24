from decimal import Decimal

from django.db import models

from uuid import uuid4




class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Deposit"
        WITHDRAW = "WITHDRAW", "Withdraw"
        DEBIT = "DEBIT", "Debit"
        CREDIT = "CREDIT", "Credit"

    account = models.ForeignKey(
        "accounts.Account",
        on_delete=models.CASCADE,
        related_name="transactions",
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    balance_after_transaction = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
    



class Transfer(models.Model):

    class Status(models.TextChoices):
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    reference_number = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
    )

    sender_account = models.ForeignKey(
        "accounts.Account",
        related_name="sent_transfers",
        on_delete=models.CASCADE,
    )

    receiver_account = models.ForeignKey(
        "accounts.Account",
        related_name="received_transfers",
        on_delete=models.CASCADE,
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUCCESS,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.reference_number)