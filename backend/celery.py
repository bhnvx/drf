import os
import datetime
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.local')

app = Celery('backend', broker='redis://localhost:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = "Asia/Seoul"
app.conf.enable_utc = False
app.now = datetime.datetime.now
