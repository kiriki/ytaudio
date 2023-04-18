from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from rest_framework import status

from django.urls import reverse

if TYPE_CHECKING:
    from rest_framework.test import APIClient

tasks_path = reverse('api:videosource-list')
yt_url = 'https://www.youtube.com/watch?v=t5edp-hLRBE'


@pytest.mark.django_db()
def test_list_tasks(anon_client: APIClient, client: APIClient):
    assert client is not anon_client

    response = anon_client.get(tasks_path, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.get(tasks_path, format='json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
def test_create_task_anon(anon_client: APIClient):
    response = anon_client.post(
        tasks_path,
        data={'url': yt_url},
        format='json',
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db()
def test_create_task(client: APIClient):
    response = client.post(
        tasks_path,
        data={'url': yt_url},
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db()
def test_tasks_flow(client: APIClient):
    tasks_count = 5

    tasks_data = [{'url': f'{yt_url}_{i}'} for i in range(tasks_count)]

    # Create
    for task_data in tasks_data:
        response = client.post(tasks_path, data=task_data)
        assert response.status_code == status.HTTP_201_CREATED, response.content
        data = response.json()
        task_data.update(data)
        assert data.get('user') == client.handler._force_user.id

    # Users count
    response = client.get(tasks_path)
    assert response.status_code == status.HTTP_200_OK, response.content

    data = response.json()
    assert data['count'] == tasks_count
