#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: celery_config.py
#  Last Modified: 2024-10-05 15:31:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 20:30:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

from config import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-and-perform-auto-top-up-every-night': {
        'task': 'apps.llm_transaction.tasks.check_and_perform_auto_topup_tasks.check_and_perform_auto_top_up',
        'schedule': crontab(minute=0, hour=0),
    },
    'randomize_featured_functions-every-6-hours': {
        'task': 'apps.mm_functions.tasks.randomize_featured_functions_tasks.randomize_featured_functions',
        'schedule': crontab(minute=0, hour='*/6'),
    },
    'randomize_featured_apis-every-6-hours': {
        'task': 'apps.mm_apis.tasks.randomize_feature_apis_tasks.randomize_featured_apis',
        'schedule': crontab(minute=0, hour='*/6'),
    },
    'randomize_featured_scripts-every-6-hours': {
        'task': 'apps.mm_scripts.tasks.randomize_featured_scripts_tasks.randomize_featured_scripts',
        'schedule': crontab(minute=0, hour='*/6'),
    },
    'track-organization-balances-every-1-hour': {
        'task': 'apps.llm_transaction.tasks.track_organization_balances_tasks.track_organization_balances',
        'schedule': crontab(minute=0, hour='*/1'),
    },
    'initiate_automated_backups-every-1-week': {
        'task': 'apps.user_settings.tasks.automated_backups_tasks.initiate_automated_backups',
        'schedule': crontab(minute=0, hour=0, day_of_week="sunday"),
    },
    'generate_daily_metatempo_logs-every-1-day': {
        'task': 'apps.metatempo.tasks.daily_metatempo_logs_processor.generate_daily_metatempo_logs',
        'schedule': crontab(hour="0", minute="30"),
    },
    'generate_period_overall_metatempo_logs-every-1-day': {
        'task': 'apps.metatempo.tasks.overall_metatempo_logs_processor.generate_period_overall_metatempo_logs',
        'schedule': crontab(hour="*", minute="*"),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


if settings.DEBUG:
    app.conf.beat_max_loop_interval = 30
else:
    app.conf.beat_max_loop_interval = 300


@app.on_after_finalize.connect
def setup_tasks(sender, **kwargs):
    print(f"Registered tasks: {app.tasks.keys()}")
