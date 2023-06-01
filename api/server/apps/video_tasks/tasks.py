import functools
import logging
import time

import yt_dlp
from asgiref.sync import async_to_sync
from celery import Task, shared_task
from channels.layers import get_channel_layer

from server.apps.video_tasks.dl_service import VideoDlService
from server.apps.video_tasks.models import VideoSource

log = logging.getLogger(__name__)


def update_ws(msg):
    # send to channel
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('tasks', msg)


@shared_task(bind=True)
def sample_task_progress(task: Task, steps: int = 10) -> int:
    log.info('sample_task_progress start')

    result = 0
    msg_data = {'task': 'sample_task_progress'}

    for k in range(steps):
        log.info('sample_task_progress progress')

        result += k
        time.sleep(1)
        progress_data = {
            'state': 'PROGRESS',
            'meta': {'current_value': result},
        }

        task.update_state(**progress_data)

        msg_data.update(progress_data)
        update_ws(
            {
                'type': 'task_update_message',
                'data': msg_data,
            }
        )

    log.info('task done')

    msg_data['state'] = 'DONE'

    update_ws(
        {
            'type': 'task_update_message',
            'data': msg_data,
        }
    )

    return result


@shared_task
def video_retrieve_metadata(video_source_id: int) -> None:
    video_source = VideoSource.objects.get(pk=video_source_id)

    try:
        metadata = VideoDlService.get_metadata(video_url=video_source.url)
    except yt_dlp.utils.DownloadError as e:
        video_source.delete()
        data = {'error': e.msg}
    else:
        video_source = VideoDlService.fill_metadata(video_source, metadata)
        data = {'action': 'reload', 'task_pk': video_source.pk}

    update_ws({'type': 'task_update_message', 'data': data})


def on_progress_download(task_id: int, data: dict) -> None:
    p_data = {
        'status': data['status'],
        'downloaded': data.get('downloaded_bytes', 0),
        'total': data.get('total_bytes') or int(data.get('total_bytes_estimate', 0)),
    }

    ws_data = {
        'task_pk': task_id,
        'progress': p_data,
    }

    update_ws({'type': 'task_update_message', 'data': ws_data})


@shared_task
def video_download_audio(*, video_source_id: int) -> None:
    log.info(f'video_download_audio, {video_source_id=}')

    video_source = VideoSource.objects.get(pk=video_source_id)

    on_progress = functools.partial(on_progress_download, video_source_id)
    result_audio_path = VideoDlService.download_audio(video_source.url, on_progress=on_progress)
    VideoDlService.store_audio(video_source, result_audio_path)

    log.info('video_download_audio done')

    data = {'action': 'reload', 'task_pk': video_source.pk}
    update_ws({'type': 'task_update_message', 'data': data})


@shared_task
def video_download_audio_mock(*, video_source_id: int) -> None:
    log.info(f'video_download_audio, {video_source_id=}')
    on_progress = functools.partial(on_progress_download, video_source_id)
    video_source = VideoSource.objects.get(pk=video_source_id)

    for k in range(50):
        time.sleep(0.1)
        data = {'status': 'downloading', 'downloaded_bytes': k, 'total_bytes': 50}
        on_progress(data)

    data = {'status': 'finished', 'downloaded_bytes': 50, 'total_bytes': 50}
    on_progress(data)

    time.sleep(2)

    data = {'action': 'reload', 'task_pk': video_source.pk}
    update_ws({'type': 'task_update_message', 'data': data})
