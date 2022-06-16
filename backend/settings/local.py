from .base import *
from .platforms.local import read_env


env = read_env(base_dir=BASE_DIR)

SECRET_KEY = env['DJANGO_SECRET_KEY']
DEBUG = True
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = 'backend.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
