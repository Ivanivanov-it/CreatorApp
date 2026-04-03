from .base import *

DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = [host for host in (os.getenv('ALLOWED_HOSTS') or "").split(',') if host]


EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False