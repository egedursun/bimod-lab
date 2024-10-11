#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: randomize_featured_scripts_tasks.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
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

from celery import shared_task

from apps.mm_scripts.models import CustomScript
from apps.mm_scripts.utils import NUMBER_OF_RANDOM_FEATURED_SCRIPTS


@shared_task
def randomize_featured_scripts():
    all_scripts = CustomScript.objects.all()
    for script in all_scripts:
        script.is_featured = False
        script.save()
    featured_scripts = CustomScript.objects.order_by('?')[:NUMBER_OF_RANDOM_FEATURED_SCRIPTS]
    for script in featured_scripts:
        script.is_featured = True
        script.save()
