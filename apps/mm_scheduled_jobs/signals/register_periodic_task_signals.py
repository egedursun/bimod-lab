#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: register_periodic_task_signals.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask

from apps.mm_scheduled_jobs.models import ScheduledJob
from apps.mm_scheduled_jobs.tasks import add_periodic_task


@receiver(post_save, sender=ScheduledJob)
def register_periodic_task(sender, instance, created, **kwargs):
    PeriodicTask.objects.filter(name=f'ScheduledJob-{instance.id}').delete()
    add_periodic_task(instance)
