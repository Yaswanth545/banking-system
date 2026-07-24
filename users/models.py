from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Custom user model for the Banking System.
    """

    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        EMPLOYEE = "employee", "Employee"
        ADMIN = "admin", "Admin"

    email = models.EmailField(
        unique=True,
        help_text="User email address used for login."
    )

    phone_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text="User's mobile number."
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email