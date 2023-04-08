from server.settings.components import config
from server.settings.components.rest_framework import REST_FRAMEWORK

# https://docs.djangoproject.com/en/4.2/howto/deployment/

DEBUG = False

ALLOWED_HOSTS = [
    'api',
    config('DOMAIN_NAME'),
    # We need this value for `healthcheck` to work:
    'localhost',
]

# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_SECONDS = 3600
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

CSRF_COOKIE_SECURE = False
# CSRF_COOKIE_HTTPONLY = False
# SESSION_COOKIE_SECURE = False

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ('rest_framework.renderers.JSONRenderer',)

CSRF_TRUSTED_ORIGINS = (f'http://*{config("DOMAIN_NAME")}/',)
