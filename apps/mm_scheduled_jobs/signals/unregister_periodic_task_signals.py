#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: unregister_periodic_task_signals.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask

from apps.mm_scheduled_jobs.models import (
    ScheduledJob,
    OrchestrationScheduledJob,
    LeanModScheduledJob,
)


@receiver(post_delete, sender=ScheduledJob)
def unregister_periodic_task(sender, instance, **kwargs):
    PeriodicTask.objects.filter(name=f'ScheduledJob-{instance.id}').delete()


@receiver(post_delete, sender=OrchestrationScheduledJob)
def unregister_periodic_task_orchestration(sender, instance, **kwargs):
    PeriodicTask.objects.filter(name=f'OrchestrationScheduledJob-{instance.id}').delete()


@receiver(post_delete, sender=LeanModScheduledJob)
def unregister_periodic_task_leanmod(sender, instance, **kwargs):
    PeriodicTask.objects.filter(name=f'LeanModScheduledJob-{instance.id}').delete()
