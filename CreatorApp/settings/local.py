from .base import *

DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = [host for host in (os.getenv('ALLOWED_HOSTS') or "").split(',') if host]


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]



EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
