import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get_own_profile(api_client, test_user):
    # Authentication
    api_client.force_authenticate(user=test_user)

    response = api_client.get("/api/v1/users/me/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "testuser"


@pytest.mark.django_db
def test_unauthenticated_me_fails(api_client):
    # Access without login
    response = api_client.get("/api/v1/users/me/")
    assert response.status_code == status.HTTP_403_FORBIDDEN
