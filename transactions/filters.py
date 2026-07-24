import django_filters

from .models import Transaction


class TransactionFilter(django_filters.FilterSet):
    """
    Filters for transaction history.
    """

    start_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__gte",
    )

    end_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__lte",
    )

    min_amount = django_filters.NumberFilter(
        field_name="amount",
        lookup_expr="gte",
    )

    max_amount = django_filters.NumberFilter(
        field_name="amount",
        lookup_expr="lte",
    )

    class Meta:
        model = Transaction
        fields = (
            "transaction_type",
        )