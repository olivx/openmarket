import logging.config

from rest_framework import viewsets

from api.exceptions import CannotPatchApiException
from api.filters import OpenMarketFilterSet
from api.models import (
    District,
    Neighborhood,
    OpenMarket,
    Region,
    SubCityHall,
    SubRegion,
)
from api.serializers import (
    DistrictSerializer,
    NeighborhoodSerializer,
    OpenMarketSerializer,
    RegionSerializer,
    SubCityHallSerializer,
    SubRegionSerializer,
)

logger = logging.getLogger(__name__)


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    name = "district"


class SubCityHallViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCityHall.objects.all()
    serializer_class = SubCityHallSerializer
    name = "subcityhall"


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    name = "region"


class SubRegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubRegion.objects.all()
    serializer_class = SubRegionSerializer
    name = "subregion"


class NeighborhoodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Neighborhood.objects.all()
    serializer_class = NeighborhoodSerializer
    name = "neighborhood"


class OpenMarketViewSet(viewsets.ModelViewSet):
    serializer_class = OpenMarketSerializer
    queryset = OpenMarket.objects.select_related(
        "neighborhood", "district", "sub_region", "sub_region__region", "sub_city_hall"
    ).all()
    name = "openmarket"
    http_method_names = ["get", "post", "head", "options", "patch", "delete"]
    filterset_fields = ("nome", "district", "neighborhood", "sub_region")
    filterset_class = OpenMarketFilterSet

    def partial_update(self, request, pk=None):
        if request.data.get("register"):
            raise CannotPatchApiException("Cannot patch [register] field")

        return super().partial_update(request, pk)
