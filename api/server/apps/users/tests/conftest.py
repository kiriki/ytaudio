from __future__ import annotations

import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

TEST_PASSWORD = 'test_pass'


@pytest.fixture
def user_with_password(user: User) -> User:
    user.set_password(TEST_PASSWORD)
    user.save()
    return user


@pytest.fixture
def jwt_tokens(user_with_password: User):
    refresh = RefreshToken.for_user(user_with_password)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
