"""
This is a django-split-settings main file.

To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""

from os import environ

# import django_stubs_ext
from split_settings.tools import include

# Managing environment via `DJANGO_ENV` variable:
environ.setdefault('DJANGO_ENV', 'development')
_ENV = environ['DJANGO_ENV']

_base_settings = (
    'components/base.py',
    'components/databases.py',
    # 'components/logging.py',
    'components/celery.py',
    'components/rest_framework.py',
    # # Select the right env:
    f'environments/{_ENV}.py',
    # # Optionally override some settings:
    # optional('environments/local.py'),
)

# Include settings:
include(*_base_settings)
