from django_filters import CharFilter, NumberFilter
from utils.filters import BaseFilterSet, OrderingFilter, SearchFilter

from .models import File


class FileFilter(BaseFilterSet):
    class Meta:
        model = File
        fields = ["name", "node_id", "hash"]
        ordering_fields = ["name", "node__name"]
        search_fields = ["name", "node__name", "hash"]

    node_id = NumberFilter(field_name="node_id")

    name = CharFilter(lookup_expr="icontains")
    hash = CharFilter()

    ordering = OrderingFilter(fields=Meta.ordering_fields)
    search = SearchFilter()
