#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask

from apps.mm_scheduled_jobs.models import ScheduledJob


@receiver(post_delete, sender=ScheduledJob)
def unregister_periodic_task(sender, instance, **kwargs):
    PeriodicTask.objects.filter(name=f'ScheduledJob-{instance.id}').delete()
