"""
This file contains all the settings that defines the development server.
SECURITY WARNING: don't run with debug turned on in production!
"""

from server.settings.components import config
from server.settings.components.databases import DATABASES

# Production flags:
# https://docs.djangoproject.com/en/2.2/howto/deployment/

DEBUG = True

ALLOWED_HOSTS = [
    config('DOMAIN_NAME'),
    'localhost',
    '0.0.0.0',  # noqa: S104
    '127.0.0.1',
    '[::1]',
]

# Static files:
# https://docs.djangoproject.com/en/4.1/ref/settings/#std:setting-STATICFILES_DIRS

# Additional locations of static files
STATICFILES_DIRS: list[str] = []

# Disable persistent DB connections
# https://docs.djangoproject.com/en/4.1/ref/databases/#caveats
DATABASES['default']['CONN_MAX_AGE'] = 0


INTERNAL_IPS = [
    '127.0.0.1',
    '192.168.7.55',
]
#
# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': lambda request: True,
# }
