from django.contrib import admin
from .models import Account
from .models import Account, AccountNumberSequence


admin.site.register(Account)



@admin.register(AccountNumberSequence)
class AccountNumberSequenceAdmin(admin.ModelAdmin):
    list_display = ("id", "last_number")