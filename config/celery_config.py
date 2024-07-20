

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'check-and-perform-auto-top-up-every-night': {
        'task': 'apps.llm_transaction.tasks.check_and_perform_auto_top_up',
        'schedule': crontab(minute=0, hour=0),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_max_loop_interval = 300

