from .platforms.deploy import read_secret
from .base import *


SECRET_KEY = read_secret('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': read_secret('DB_PASSWORD'),
        'HOST': 'postgresql',
        'PORT': 5432

    }
}