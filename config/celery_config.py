

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

from config import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # PERFORM AUTOMATIC BALANCE TOP-UP OPERATIONS (1/24 hours)
    'check-and-perform-auto-top-up-every-night': {
        'task': 'apps.llm_transaction.tasks.check_and_perform_auto_top_up',
        'schedule': crontab(minute=0, hour=0),
    },
    # PERFORM RANDOM FEATURED FUNCTION ASSIGNMENT (1/6 hours)
    'randomize_featured_functions-every-6-hours': {
        'task': 'apps.mm_functions.tasks.randomize_featured_functions',
        'schedule': crontab(minute=0, hour='*/6'),
    },
    # PERFORM RANDOM FEATURED API ASSIGNMENT (1/6 hours)
    'randomize_featured_apis-every-6-hours': {
        'task': 'apps.mm_apis.tasks.randomize_featured_apis',
        'schedule': crontab(minute=0, hour='*/6'),
    },
    # PERFORM RANDOM FEATURED SCRIPT ASSIGNMENT (1/6 hours)
    'randomize_featured_scripts-every-6-hours': {
        'task': 'apps.mm_scripts.tasks.randomize_featured_scripts',
        'schedule': crontab(minute=0, hour='*/6'),
    },
    # CRON TASK TO TRACK ORGANIZATION BALANCE SNAPSHOTS
    'track-organization-balances-every-1-hour': {
        'task': 'apps.llm_transaction.tasks.track_organization_balances',
        'schedule': crontab(minute=0, hour='*/1'),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# refresh more frequently for debugging
if settings.DEBUG:
    app.conf.beat_max_loop_interval = 30
else:
    app.conf.beat_max_loop_interval = 300


############################################
# FOR TESTING ONLY
############################################
# app.send_task('apps.mm_scheduled_jobs.tasks.execute_scheduled_job', args=[9])

