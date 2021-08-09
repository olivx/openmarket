import pytest
from django.urls import reverse
from model_mommy import mommy

from api.models import (
    District,
    Neighborhood,
    OpenMarket,
    Region,
    SubCityHall,
    SubRegion,
)


@pytest.mark.django_db(transaction=True)
def test_list_districts(api_client):
    mommy.make(District, _quantity=10)
    resp = api_client.get(reverse("district-list"))

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 10


@pytest.mark.django_db(transaction=True)
def test_get_district_by_id(api_client, django_request):
    district = mommy.make(District)
    resp = api_client.get(reverse("district-detail", args=([district.id])))

    assert resp.status_code == 200
    assert (
        django_request.build_absolute_uri(
            reverse("district-detail", args=([district.id]))
        )
        == resp.json()["url"]
    )


@pytest.mark.django_db(transaction=True)
def test_list_sub_city_halleituras(api_client):
    mommy.make(SubCityHall, _quantity=10)
    resp = api_client.get(reverse("subcityhall-list"))

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 10


@pytest.mark.django_db(transaction=True)
def test_get_sub_city_halleitura_by_id(api_client, django_request):
    sub_city_halleitura = mommy.make(SubCityHall)
    resp = api_client.get(
        reverse("subcityhall-detail", args=([sub_city_halleitura.id]))
    )

    assert resp.status_code == 200
    assert (
        django_request.build_absolute_uri(
            reverse("subcityhall-detail", args=([sub_city_halleitura.id]))
        )
        == resp.json()["url"]
    )


@pytest.mark.django_db(transaction=True)
def test_list_region(api_client):
    mommy.make(Region, _quantity=10)
    resp = api_client.get(reverse("region-list"))

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 10


@pytest.mark.django_db(transaction=True)
def test_get_region_by_id(api_client, django_request):
    region = mommy.make(Region)
    resp = api_client.get(reverse("region-detail", args=([region.id])))

    assert resp.status_code == 200
    assert (
        django_request.build_absolute_uri(reverse("region-detail", args=([region.id])))
        == resp.json()["url"]
    )


@pytest.mark.django_db(transaction=True)
def test_list_sub_region(api_client):
    mommy.make(SubRegion, _quantity=10)
    resp = api_client.get(reverse("subregion-list"))

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 10


@pytest.mark.django_db(transaction=True)
def test_get_sub_region_by_id(api_client, django_request):
    sub_region = mommy.make(SubRegion)
    resp = api_client.get(reverse("subregion-detail", args=([sub_region.id])))

    assert resp.status_code == 200
    assert (
        django_request.build_absolute_uri(
            reverse("subregion-detail", args=([sub_region.id]))
        )
        == resp.json()["url"]
    )


@pytest.mark.django_db(transaction=True)
def test_list_neighborhoods(api_client):
    mommy.make(Neighborhood, _quantity=10)
    resp = api_client.get(reverse("neighborhood-list"))

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 10


@pytest.mark.django_db(transaction=True)
def test_get_neighborhood_by_id(api_client, django_request):
    neighborhood = mommy.make(Neighborhood)
    resp = api_client.get(reverse("neighborhood-detail", args=([neighborhood.id])))

    assert resp.status_code == 200
    assert (
        django_request.build_absolute_uri(
            reverse("neighborhood-detail", args=([neighborhood.id]))
        )
        == resp.json()["url"]
    )


@pytest.mark.django_db(transaction=True)
def test_list_openmarkets(api_client):
    mommy.make(OpenMarket, _quantity=10)
    resp = api_client.get(reverse("openmarket-list"))

    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 10


@pytest.mark.django_db(transaction=True)
def test_get_openmarket_by_id(api_client, django_request):
    openmarket = mommy.make(OpenMarket)
    resp = api_client.get(reverse("openmarket-detail", args=([openmarket.id])))

    assert resp.status_code == 200
    assert (
        django_request.build_absolute_uri(
            reverse("openmarket-detail", args=([openmarket.id]))
        )
        == resp.json()["url"]
    )


@pytest.mark.django_db(transaction=True)
def test_create_openmarket(api_client):
    openmarket = mommy.prepare(OpenMarket, register="9641-0", _save_related=True)
    data = dict(
        name=openmarket.name,
        location="POINT (13.0078125000020002 42.4234565179379999)",
        register=openmarket.register,
        area=openmarket.area,
        sector=openmarket.sector,
        public_place=openmarket.public_place,
        number=openmarket.number,
        ref=openmarket.ref,
        district_id=openmarket.district_id,
        sub_city_hall_id=openmarket.sub_city_hall_id,
        sub_region_id=openmarket.sub_region_id,
        neighborhood_id=openmarket.neighborhood_id,
    )
    resp = api_client.post(reverse("openmarket-list"), data=data, format="json")
    assert resp.status_code == 201
    assert OpenMarket.objects.get(register=data["register"])


@pytest.mark.django_db(transaction=True)
def test_create_openmarket_required_fields(api_client):
    data = {}
    resp = api_client.post(reverse("openmarket-list"), data=data, format="json")

    assert resp.status_code == 400
    assert resp.json() == {
        "neighborhood_id": ["This field is required."],
        "district_id": ["This field is required."],
        "sub_city_hall_id": ["This field is required."],
        "sub_region_id": ["This field is required."],
        "name": ["This field is required."],
        "register": ["This field is required."],
        "location": ["This field is required."],
        "sector": ["This field is required."],
        "area": ["This field is required."],
        "public_place": ["This field is required."],
        "ref": ["This field is required."],
    }


@pytest.mark.django_db(transaction=True)
def test_query_openmarket_by_name(api_client):
    openmarket = mommy.make(OpenMarket)

    resp = api_client.get("%s?name=%s" % (reverse("openmarket-list"), openmarket.name))

    assert resp.status_code == 200
    assert resp.json()["results"][0]["name"] == openmarket.name


@pytest.mark.django_db(transaction=True)
def test_query_openmarket_by_district(api_client):
    openmarket = mommy.make(OpenMarket)

    resp = api_client.get(
        "%s?district=%s" % (reverse("openmarket-list"), openmarket.district.name)
    )

    assert resp.status_code == 200
    assert resp.json()["results"][0]["name"] == openmarket.name


@pytest.mark.django_db(transaction=True)
def test_query_openmarket_by_neighborhood(api_client):
    openmarket = mommy.make(OpenMarket)

    resp = api_client.get(
        "%s?neighborhood=%s"
        % (reverse("openmarket-list"), openmarket.neighborhood.name)
    )

    assert resp.status_code == 200
    assert resp.json()["results"][0]["name"] == openmarket.name


@pytest.mark.django_db(transaction=True)
def test_query_openmarket_by_region(api_client):
    openmarket = mommy.make(OpenMarket)

    resp = api_client.get(
        "%s?region=%s" % (reverse("openmarket-list"), openmarket.sub_region.region.name)
    )

    assert resp.status_code == 200
    assert resp.json()["results"][0]["name"] == openmarket.name


@pytest.mark.django_db(transaction=True)
def test_delete_openmarket(api_client):
    openmarket = mommy.make(OpenMarket)
    assert len(OpenMarket.objects.all()) == 1

    resp = api_client.delete(reverse("openmarket-detail", args=([openmarket.id])))

    assert resp.status_code == 204
    assert len(OpenMarket.objects.all()) == 0


@pytest.mark.django_db(transaction=True)
def test_patch_openmarket(api_client):
    openmarket = mommy.make(OpenMarket)
    data = {"name": "Feira do Carlos Blanka"}
    resp = api_client.patch(
        reverse("openmarket-detail", args=([openmarket.id])), data=data
    )

    assert resp.status_code == 200
    assert resp.json()["name"] == data["name"].upper()


@pytest.mark.django_db(transaction=True)
def test_cannot_patch_openmarket_register(api_client):
    openmarket = mommy.make(OpenMarket)
    data = {"name": "Feira do Carlos Blanka", "register": "8979"}
    resp = api_client.patch(
        reverse("openmarket-detail", args=([openmarket.id])), data=data
    )

    assert resp.status_code == 400
    assert resp.json() == {"detail": "Cannot patch [register] field"}


@pytest.mark.django_db(transaction=True)
def test_cannot_put_openmarket(api_client):
    openmarket = mommy.make(OpenMarket)
    data = {"name": "Feira do Carlos Blanka", "register": "8979"}
    resp = api_client.put(
        reverse("openmarket-detail", args=([openmarket.id])), data=data
    )

    assert resp.status_code == 405
    assert resp.json() == {"detail": 'Method "PUT" not allowed.'}
