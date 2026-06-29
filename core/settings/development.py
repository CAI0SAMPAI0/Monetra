from .base import *
from decouple import config, Csv
import dj_database_url

DEBUG = config('DEBUG', default=True, cast=bool)

#ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': dj_database_url.config(
        default=config('NEON_POSTGRESQL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Cookie settings for cross-origin local development (frontend on :8080, backend on :8000)
# SameSite=None allows cross-origin cookie sending.
# Browsers require Secure=True when SameSite=None, even on localhost.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'

# Additional CORS origins for local static frontend server
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:5500',
    'http://127.0.0.1:5500',
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'https://monetra-coral-two.vercel.app',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:5500',
    'http://127.0.0.1:5500',
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'https://*.vercel.app',
]


