import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    """Global API Client"""
    return APIClient()


@pytest.fixture
def test_user(db):
    """Global test_user"""
    return User.objects.create_user(username="testuser", password="password123")
