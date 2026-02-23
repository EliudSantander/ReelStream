import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from .models import Watchlist


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="test_user", password="password123")


@pytest.fixture
def test_user_2(db):
    return User.objects.create_user(username="test_user_2", password="password123")


@pytest.mark.django_db
class TestWatchlistEndpoints:

    # --- GET WATCHLIST ---
    def test_get_watchlist(self, api_client, test_user):
        Watchlist.objects.create(user=test_user, film_id=1)

        api_client.force_authenticate(user=test_user)
        response = api_client.get("/api/v1/watchlist/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["film"]["film_id"] == 1

    def test_retrieve_watchlist(self, api_client, test_user):
        user_item = Watchlist.objects.create(user=test_user, film_id=1)

        api_client.force_authenticate(user=test_user)
        response = api_client.get(f"/api/v1/watchlist/{user_item.id}/")

        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_other_user_watchlist_fails(
        self, api_client, test_user, test_user_2
    ):
        item_other_user = Watchlist.objects.create(user=test_user_2, film_id=1)

        api_client.force_authenticate(user=test_user)
        response = api_client.get(f"/api/v1/watchlist/{item_other_user.id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # --- CREATE WATCHLIST ---
    def test_create_watchlist(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        data = {"film_id": 1}
        response = api_client.post("/api/v1/watchlist/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Watchlist.objects.filter(user=test_user, film_id=1).exists()

    def test_prevent_duplicate_watchlist(self, api_client, test_user):
        Watchlist.objects.create(user=test_user, film_id=1)
        api_client.force_authenticate(user=test_user)

        response = api_client.post("/api/v1/watchlist/", {"film_id": 1})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "detail" in response.data

    # --- DELETE WATCHLIST ---
    def test_delete_watchlist(self, api_client, test_user):
        item = Watchlist.objects.create(user=test_user, film_id=1)
        api_client.force_authenticate(user=test_user)

        response = api_client.delete(f"/api/v1/watchlist/{item.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Watchlist.objects.filter(id=item.id).exists()
