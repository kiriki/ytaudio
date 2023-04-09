# Celery application definition
# https://docs.celeryq.dev/en/v5.2.7/userguide/configuration.html
from . import config

CELERY_BROKER_URL = f'redis://{config("REDIS_HOST")}'
CELERY_RESULT_BACKEND = f'redis://{config("REDIS_HOST")}'
# CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True

CELERY_ACCEPT_CONTENT = ['application/json']  # 'pickle'

CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Europe/Moscow'

# CELERY_BEAT_SCHEDULE = {
#     'task-number-one': {
#         'task': 'reddit.tasks.periodic_task_one',
#         'schedule': 600.0,
#         # 'schedule': crontab(minute='*/1'),
#         # 'schedule': crontab(minute=59, hour=23),
#         # 'args': (1, 4)
#     },
# }

# CELERY_TRACK_STARTED = True

# CELERY_ALWAYS_EAGER = True
# CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
# CELERY_TASK_TRACK_STARTED = True
