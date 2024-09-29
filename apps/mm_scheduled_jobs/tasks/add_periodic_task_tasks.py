#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: add_periodic_task_tasks.py
#  Last Modified: 2024-09-28 20:38:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:02:16
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import json

from django_celery_beat.models import CrontabSchedule, PeriodicTask


def add_periodic_task(scheduled_job):
    crontab_schedule, created = CrontabSchedule.objects.get_or_create(
        minute=scheduled_job.minute or '*',
        hour=scheduled_job.hour or '*',
        day_of_week=scheduled_job.day_of_week or '*',
        day_of_month=scheduled_job.day_of_month or '*',
        month_of_year=scheduled_job.month_of_year or '*'
    )
    PeriodicTask.objects.create(
        crontab=crontab_schedule,
        name=f'ScheduledJob-{scheduled_job.id}',
        task='apps.mm_scheduled_jobs.tasks.execute_scheduled_job',
        args=json.dumps([scheduled_job.id])
    )
