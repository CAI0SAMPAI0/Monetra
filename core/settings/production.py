from .base import *
from decouple import config, Csv
import dj_database_url

DEBUG = False

import os

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default='')

# Auto-add Render external hostname if running on Render
if 'RENDER_EXTERNAL_HOSTNAME' in os.environ:
    render_host = os.environ['RENDER_EXTERNAL_HOSTNAME']
    if isinstance(ALLOWED_HOSTS, str):
        ALLOWED_HOSTS = [ALLOWED_HOSTS] if ALLOWED_HOSTS else []
    elif not isinstance(ALLOWED_HOSTS, list):
        ALLOWED_HOSTS = list(ALLOWED_HOSTS)
    if render_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(render_host)

# Auto-add Hugging Face host if running on Hugging Face Spaces
if 'SPACE_HOST' in os.environ:
    space_host = os.environ['SPACE_HOST']
    if isinstance(ALLOWED_HOSTS, str):
        ALLOWED_HOSTS = [ALLOWED_HOSTS] if ALLOWED_HOSTS else []
    elif not isinstance(ALLOWED_HOSTS, list):
        ALLOWED_HOSTS = list(ALLOWED_HOSTS)
    if space_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(space_host)

# Configure CSRF trusted origins for production (needed for form submissions)
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv(), default='')
if isinstance(CSRF_TRUSTED_ORIGINS, str):
    CSRF_TRUSTED_ORIGINS = [CSRF_TRUSTED_ORIGINS] if CSRF_TRUSTED_ORIGINS else []
else:
    CSRF_TRUSTED_ORIGINS = list(CSRF_TRUSTED_ORIGINS)

# Automatically trust Hugging Face subdomains
if 'https://*.hf.space' not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append('https://*.hf.space')

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
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
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

# Logging configuration to output tracebacks to the console in production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

