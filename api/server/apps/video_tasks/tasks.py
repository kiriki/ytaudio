import time

from celery import shared_task


@shared_task
def sample_task(task_type: int) -> int:
    print('task start')
    res = int(task_type) * 10
    time.sleep(res)
    print('task done')
    return res
