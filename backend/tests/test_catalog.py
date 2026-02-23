import pytest
from rest_framework import status


@pytest.mark.django_db
class TestFilmEndpoints:

    # --- AUTHENTICATION ---
    def test_list_films_unauthenticated_fails(self, api_client):
        response = api_client.get("/api/v1/films/")

        assert response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        ]

    def test_retrieve_film_unauthenticated_fails(self, api_client):
        response = api_client.get("/api/v1/films/1/")

        assert response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        ]

    # --- HAPPY PATHS ---
    def test_list_films_authenticated(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        response = api_client.get("/api/v1/films/")

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data["results"]) > 0

    def test_retrieve_specific_film(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)

        response = api_client.get("/api/v1/films/1/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "ACADEMY DINOSAUR"
        assert "release_year" in response.data

    # --- EDGE CASES ---
    def test_film_not_found(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        response = api_client.get("/api/v1/films/999999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
