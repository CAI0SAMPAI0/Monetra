from .base import *
from decouple import config, Csv
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Database configuration for production
# Using dj_database_url to parse the DATABASE_URL environment variable
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=config('NEON_POSTGRESQL', default='')),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Static files storage for production
# Using whitenoise for compression and caching
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}
