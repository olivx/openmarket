import pytest
from django.contrib.gis.geos import fromstr

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


@pytest.mark.django_db(transaction=True)
def test_deserialize_district(django_request):
    model = District.objects.create(name="Vila Formosa")
    serializer = DistrictSerializer(model, context={"request": django_request})

    for f in model._meta.fields:
        assert f.name in serializer.data.keys() if f.name != "id" else True


@pytest.mark.django_db(transaction=True)
def test_deserialize_sub_city_halleitura(django_request):
    model = SubCityHall.objects.create(name="Vila Prudente")
    serializer = SubCityHallSerializer(model, context={"request": django_request})

    for f in model._meta.fields:
        assert f.name in serializer.data.keys() if f.name != "id" else True


@pytest.mark.django_db(transaction=True)
def test_deserialize_region(django_request):
    model = Region.objects.create(name="Leste")
    serializer = RegionSerializer(model, context={"request": django_request})

    for f in model._meta.fields:
        assert f.name in serializer.data.keys() if f.name != "id" else True


@pytest.mark.django_db(transaction=True)
def test_deserialize_sub_region(django_request):
    region = Region.objects.create(name="Oeste")
    model = SubRegion.objects.create(name="Oeste 1", region=region)
    serializer = SubRegionSerializer(model, context={"request": django_request})

    for f in model._meta.fields:
        assert f.name in serializer.data.keys() if f.name != "id" else True


@pytest.mark.django_db(transaction=True)
def test_deserialize_neighborhood(django_request):
    model = Neighborhood.objects.create(name="Bras")
    serializer = NeighborhoodSerializer(model, context={"request": django_request})

    for f in model._meta.fields:
        assert f.name in serializer.data.keys() if f.name != "id" else True


@pytest.mark.django_db(transaction=True)
def test_deserialize_openmarket(django_request):

    district = District.objects.create(name="Vila Formosa")
    sub_city_hall = SubCityHall.objects.create(name="Vila Prudente")
    region = Region.objects.create(name="Oeste")
    sub_region = SubRegion.objects.create(name="Oeste 1", region=region)
    neighborhood = Neighborhood.objects.create(name="Bras")
    model = OpenMarket.objects.create(
        location=fromstr("POINT(-46550164 -23558733)", srid=4326),
        sector="355030885000091",
        area="3550308005040",
        name="Vila Formosa",
        register="4041-0",
        public_place="RUA MARAGOJIPE",
        number="755",
        ref="TV Rua Pretoria",
        district=district,
        sub_city_hall=sub_city_hall,
        sub_region=sub_region,
        neighborhood=neighborhood,
    )
    serializer = OpenMarketSerializer(model, context={"request": django_request})

    for f in model._meta.fields:
        assert f.name in serializer.data.keys() if f.name != "id" else True


@pytest.mark.django_db(transaction=True)
def test_serialize_openmarket_uppercase(django_request):
    district = District.objects.create(name="Vila Formosa")
    sub_city_hall = SubCityHall.objects.create(name="Vila Prudente")
    region = Region.objects.create(name="Oeste")
    sub_region = SubRegion.objects.create(name="Oeste 1", region=region)
    neighborhood = Neighborhood.objects.create(name="Bras")
    data = dict(
        location=fromstr("POINT(-46550164 -23558733)", srid=4326),
        name="vila formosa",
        register="TEST-0",
        public_place="rua maragojipe",
        sector="355030885000091",
        area="3550308005040",
        number="755",
        ref="tv rua pretoria",
        district_id=district.id,
        sub_city_hall_id=sub_city_hall.id,
        sub_region_id=sub_region.id,
        neighborhood_id=neighborhood.id,
    )
    serializer = OpenMarketSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    open_market = OpenMarket.objects.get(register="TEST-0")
    assert open_market.public_place == "RUA MARAGOJIPE"
    assert open_market.ref == "TV RUA PRETORIA"
    assert open_market.name == "VILA FORMOSA"
