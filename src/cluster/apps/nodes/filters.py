from django_filters import CharFilter
from utils.filters import BaseFilterSet, OrderingFilter, SearchFilter

from .models import Node


class NodeFilter(BaseFilterSet):
    class Meta:
        model = Node
        fields = ["name"]
        ordering_fields = ["name"]
        search_fields = ordering_fields

    name = CharFilter(lookup_expr="icontains")

    ordering = OrderingFilter(fields=Meta.ordering_fields)

    search = SearchFilter()
