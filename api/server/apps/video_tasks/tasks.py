import logging
import time

from asgiref.sync import async_to_sync
from celery import Task, shared_task
from channels.layers import get_channel_layer

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
