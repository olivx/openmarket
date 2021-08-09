import django_filters
from django_filters import rest_framework as filters

from api.models import OpenMarket


class OpenMarketFilterSet(filters.FilterSet):
    district = django_filters.CharFilter(
        field_name="district", lookup_expr="name__iexact"
    )
    neighborhood = django_filters.CharFilter(
        field_name="neighborhood", lookup_expr="name__iexact"
    )
    region = django_filters.CharFilter(
        field_name="sub_region", lookup_expr="region__name__iexact"
    )

    class Meta:
        model = OpenMarket
        fields = ["name", "district", "neighborhood", "region"]
