from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

if TYPE_CHECKING:
    from rest_framework.test import APIClient

    from django.contrib.auth.models import User

TEST_PASSWORD = 'test_pass'

users_path = reverse('api:user-list')


@pytest.fixture
def user_with_password(user: User) -> User:
    user.set_password(TEST_PASSWORD)
    user.save()
    return user


@pytest.mark.django_db()
def test_auth_using_login_pass(anon_client: APIClient, user_with_password: User):
    username = user_with_password.username
    response = anon_client.post(
        '/api/auth/login/',
        data={'username': username, 'password': 'incorrect_password'},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = anon_client.post(
        '/api/auth/login/',
        data={'username': username, 'password': TEST_PASSWORD},
    )
    assert response.status_code == status.HTTP_200_OK, response.content

    data = response.json()

    assert data['username'] == username


@pytest.mark.django_db()
def test_user_flow(admin_client: APIClient, anon_client: APIClient):
    users_count = 5

    users_data = [
        {
            'username': f'user_{i}',
            'password': f'password_{i}',
            'email': f'email_{i}@mail.ru',
        }
        for i in range(users_count)
    ]

    assert admin_client is not anon_client

    # Create
    for user_data in users_data:
        response = admin_client.post(users_path, data=user_data)
        assert response.status_code == status.HTTP_201_CREATED, response.content
        data = response.json()
        user_data.update(data)

    # Users count
    response = admin_client.get(users_path)
    assert response.status_code == status.HTTP_200_OK, response.content

    data = response.json()
    assert data['count'] == users_count

    # Test login
    for user_data in users_data:
        user_data_login = {
            'username': user_data['username'],
            'password': user_data['password'],
        }
        response = anon_client.post('/api/auth/login/', data=user_data_login)
        assert response.status_code == status.HTTP_200_OK, response.content

    # Delete users
    for user_data in users_data:
        response = admin_client.delete(f'{users_path}{user_data["id"]}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content

    response = admin_client.get(users_path)
    assert response.status_code == status.HTTP_200_OK, response.content

    data = response.json()
    assert data['count'] == 0


@pytest.mark.django_db()
def test_api_auth_logout(admin_client):
    response = admin_client.post('/api/auth/logout/')
    assert response.status_code == status.HTTP_200_OK, response.content
