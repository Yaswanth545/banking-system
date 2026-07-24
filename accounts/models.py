from decimal import Decimal

from django.conf import settings
from django.db import models


class Account(models.Model):

    class AccountType(models.TextChoices):
        SAVINGS = "SAVINGS", "Savings"
        CURRENT = "CURRENT", "Current"

    class AccountStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        FROZEN = "FROZEN", "Frozen"
        CLOSED = "CLOSED", "Closed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accounts",
    )

    account_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )

    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.SAVINGS,
    )

    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    currency = models.CharField(
        max_length=3,
        default="INR",
    )

    status = models.CharField(
        max_length=20,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.account_number} - {self.user.email}"
    

class AccountNumberSequence(models.Model):
    """
    Stores the latest generated account number.
    """

    last_number = models.BigIntegerField(
        default=100000000000
    )

    def __str__(self):
        return str(self.last_number)
    

class Beneficiary(models.Model):
    """
    Saved beneficiary for quick money transfers.
    """

    owner = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        related_name="beneficiaries",
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="beneficiary_accounts",
    )

    nickname = models.CharField(
        max_length=100,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "account"],
                name="unique_owner_beneficiary",
            )
        ]

    def __str__(self):
        return f"{self.owner.email} -> {self.nickname}"