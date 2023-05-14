from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from rest_framework import status

from django.urls import reverse

from server.apps.video_tasks.dl_service import VideoDlService, VideoMetadata
from server.apps.video_tasks.models import VideoSource

if TYPE_CHECKING:
    from rest_framework.test import APIClient

    from django.contrib.auth.models import User

tasks_path = reverse('api:videosource-list')
yt_url = 'https://www.youtube.com/watch?v=A37eEkFALxc'
metadata_path = Path(__file__).parent / Path('data/video_metadata_fixture.json')


@pytest.mark.django_db
def test_list_tasks(anon_client: APIClient, client: APIClient):
    assert client is not anon_client

    response = anon_client.get(tasks_path, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.get(tasks_path, format='json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_task_anon(anon_client: APIClient):
    response = anon_client.post(
        tasks_path,
        data={'url': yt_url},
        format='json',
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_task(client: APIClient):
    response = client.post(
        tasks_path,
        data={'url': yt_url},
        format='json',
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
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


@pytest.fixture
def video_source_clear(user: User) -> VideoSource:
    return VideoSource.objects.create(url=yt_url, user=user)


@pytest.fixture
def metadata() -> VideoMetadata:
    with metadata_path.open() as metadata_file:
        return VideoMetadata(**json.load(metadata_file))


@pytest.fixture
def video_source(video_source_clear: VideoSource, metadata: VideoMetadata) -> VideoSource:
    VideoDlService.fill_metadata(video_source_clear, metadata)
    return VideoSource.objects.get(pk=video_source_clear.pk)


@pytest.mark.django_db
def test_fill_metadata(video_source_clear: VideoSource, metadata: VideoMetadata):
    VideoDlService.fill_metadata(video_source_clear, metadata)
    video_source = VideoSource.objects.get(pk=video_source_clear.pk)

    assert video_source.title
    assert video_source.source_id
    assert video_source.extractor
    assert video_source.channel
    assert video_source.duration > 0
    assert video_source.thumbnail


@pytest.mark.django_db
@pytest.mark.slow
def test_download_audio(video_source: VideoSource):
    result_path = VideoDlService.download_audio(video_source.url)
    assert isinstance(result_path, Path)
    assert result_path.exists()
    result_path.unlink(missing_ok=True)


@pytest.mark.django_db
def test_store_audio(video_source: VideoSource):
    VideoDlService.store_audio(video_source, metadata_path)

    video_source = VideoSource.objects.get(pk=video_source.pk)

    assert Path(video_source.file.path).exists()
    assert video_source.file_size > 0

    video_source.file.delete()
