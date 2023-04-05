from __future__ import annotations

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from django.urls import reverse

TEST_PASSWORD = 'test_pass'


@pytest.fixture
def user_with_password(user: User) -> User:
    user.set_password(TEST_PASSWORD)
    user.save()
    return user


@pytest.mark.django_db()
def test_login_jwt(anon_client: APIClient, user_with_password: User):
    """
    Ensure we can create a new account object.
    """

    jwtlogin_url = reverse('token_obtain_pair')
    username = user_with_password.username

    u1creds = {'username': username, 'password': TEST_PASSWORD}
    u2creds = {'username': username, 'password': 'incorrect_password'}

    response = anon_client.post(jwtlogin_url, u2creds, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = anon_client.post(jwtlogin_url, u1creds, format='json')
    assert response.status_code == status.HTTP_200_OK

    assert 'refresh' in response.data
    assert 'access' in response.data


@pytest.fixture
def jwt_tokens(user_with_password: User):
    refresh = RefreshToken.for_user(user_with_password)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@pytest.fixture
def jwt_tokens_admin(admin: User):
    refresh = RefreshToken.for_user(admin)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@pytest.mark.django_db()
def test_auth_jwt(anon_client: APIClient, jwt_tokens, jwt_tokens_admin):
    users_list_url = reverse('api:user-list')

    response = anon_client.get(users_list_url, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    anon_client.credentials(HTTP_AUTHORIZATION='JWT ' + jwt_tokens_admin['access'])
    response = anon_client.get(users_list_url, format='json')
    assert response.status_code == status.HTTP_200_OK

    anon_client.credentials(HTTP_AUTHORIZATION='JWT ' + jwt_tokens['access'])
    response = anon_client.get(users_list_url, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
