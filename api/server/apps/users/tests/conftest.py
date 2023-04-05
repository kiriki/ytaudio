import pytest
from rest_framework.test import APIClient

from django.contrib.auth.models import User

TEST_USER = 'test_user'
ADMIN_NAME = 'admin'


@pytest.fixture
def anon_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user() -> User:
    return User.objects.create_user(username=TEST_USER, is_superuser=True)


@pytest.fixture
def client(anon_client: APIClient, user: User) -> APIClient:
    anon_client.force_authenticate(user)
    return anon_client


@pytest.fixture
def admin() -> User:
    return User.objects.create_user(username=ADMIN_NAME, is_staff=True)


@pytest.fixture
def admin_client(admin: User) -> APIClient:
    client = APIClient()
    client.force_authenticate(admin)
    return client
