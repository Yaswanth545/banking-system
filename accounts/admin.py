from django.contrib import admin
from .models import Account
from .models import Account, AccountNumberSequence,Beneficiary


admin.site.register(Account)



@admin.register(AccountNumberSequence)
class AccountNumberSequenceAdmin(admin.ModelAdmin):
    list_display = ("id", "last_number")



@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "nickname",
        "account",
        "created_at",
    )

    search_fields = (
        "owner__email",
        "nickname",
        "account__account_number",
    )

    list_filter = (
        "created_at",
    )

    ordering = ("-created_at",)