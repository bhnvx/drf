import os
import datetime
from celery import Celery


os.environ.setdefault('DJANGO_SETTING_MODULE', 'backend.settings.local')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = "Asia/Seoul"
app.conf.enable_utc = False
app.now = datetime.datetime.now

"""
local start : celery -A backend worker -l info --concurrency=1 -P gevent
deploy start : ?
"""