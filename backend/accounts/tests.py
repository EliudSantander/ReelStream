import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    return User.objects.create_user(username="testuser", password="password123")


@pytest.mark.django_db
def test_get_own_profile(api_client, create_user):
    # Authentication
    api_client.force_authenticate(user=create_user)

    response = api_client.get("/api/v1/users/me/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "testuser"


@pytest.mark.django_db
def test_unauthenticated_me_fails(api_client):
    # Access without login
    response = api_client.get("/api/v1/users/me/")
    assert response.status_code == status.HTTP_403_FORBIDDEN
