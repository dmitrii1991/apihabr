import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apihabr.settings')

app = Celery('apihabr')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'parse-everyday-habr': {
        'task': 'api.tasks.celery_parse_habr_everyday',
        'schedule': crontab(minute=0, hour='12,15,18,21'),
    }
}

