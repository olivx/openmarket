import pytest
from rest_framework.test import APIClient, APIRequestFactory


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def django_request():
    request_factory = APIRequestFactory()
    return request_factory.get("/")
