from .base import *
from decouple import config, Csv
import dj_database_url

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

DATABASES = {
    'default': dj_database_url.config(
        default=config('NEON_POSTGRESQL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

