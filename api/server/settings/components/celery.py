# Celery application definition
# http://docs.celeryproject.org/en/v4.1.0/userguide/configuration.html

CELERY_BROKER_URL = 'redis://localhost'
# CELERY_RESULT_BACKEND = 'redis://localhost'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True

CELERY_ACCEPT_CONTENT = ['pickle', 'application/json']

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
