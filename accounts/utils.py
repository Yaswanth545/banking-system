from django.db import transaction

from .models import AccountNumberSequence


def generate_account_number():
    """
    Generate a unique sequential account number.
    """

    with transaction.atomic():

        sequence, _ = AccountNumberSequence.objects.select_for_update().get_or_create(
            pk=1,
            defaults={
                "last_number": 100000000000
            }
        )

        sequence.last_number += 1

        sequence.save(update_fields=["last_number"])

        return str(sequence.last_number)