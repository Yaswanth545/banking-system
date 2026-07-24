import django_filters

from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    """
    Filters for transaction history.
    """

    created_at_after = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__gte",
    )

    created_at_before = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__lte",
    )

    class Meta:
        model = Transaction
        fields = [
            "transaction_type",
        ]