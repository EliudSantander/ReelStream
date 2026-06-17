import pytest
from django.contrib.auth.models import User
from rest_framework import status

from interactions.models import Watched


@pytest.fixture
def test_user_2(db):
    return User.objects.create_user(username="testuser2", password="password123")


@pytest.mark.django_db
class TestWatchlistEndpoints:

    # --- GET WATCHED FILMS ---
    def test_get_watched(self, api_client, test_user):
        Watched.objects.create(user=test_user, film_id=1)

        api_client.force_authenticate(user=test_user)
        response = api_client.get("/api/v1/watched/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["film"]["film_id"] == 1

    def test_retrieve_watched(self, api_client, test_user):
        user_item = Watched.objects.create(user=test_user, film_id=1)

        api_client.force_authenticate(user=test_user)
        response = api_client.get(f"/api/v1/watched/{user_item.id}/")

        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_other_user_watched_fails(
        self, api_client, test_user, test_user_2
    ):
        item_other_user = Watched.objects.create(user=test_user_2, film_id=1)

        api_client.force_authenticate(user=test_user)
        response = api_client.get(f"/api/v1/watched/{item_other_user.id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # --- CREATE WATCHED ---
    def test_create_watched(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        data = {"film_id": 1}
        response = api_client.post("/api/v1/watched/", data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Watched.objects.filter(user=test_user, film_id=1).exists()

    def test_prevent_duplicate_watched(self, api_client, test_user):
        Watched.objects.create(user=test_user, film_id=1)
        api_client.force_authenticate(user=test_user)

        response = api_client.post("/api/v1/watched/", {"film_id": 1})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "detail" in response.data

    # --- DELETE WATCHED ---
    def test_delete_watched(self, api_client, test_user):
        item = Watched.objects.create(user=test_user, film_id=1)
        api_client.force_authenticate(user=test_user)

        response = api_client.delete(f"/api/v1/watched/{item.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Watched.objects.filter(id=item.id).exists()
