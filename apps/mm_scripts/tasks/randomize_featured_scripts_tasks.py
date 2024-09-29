#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: randomize_featured_scripts_tasks.py
#  Last Modified: 2024-09-27 19:28:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:03:08
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from celery import shared_task

from apps.mm_scripts.models import CustomScript
from apps.mm_scripts.utils import NUMBER_OF_RANDOM_FEATURED_SCRIPTS


@shared_task
def randomize_featured_scripts():
    # first switch all script's is_featured field to false
    all_scripts = CustomScript.objects.all()
    for script in all_scripts:
        script.is_featured = False
        script.save()
    # then select 5 random scripts and set the is_featured field to true
    featured_scripts = CustomScript.objects.order_by('?')[:NUMBER_OF_RANDOM_FEATURED_SCRIPTS]
    for script in featured_scripts:
        script.is_featured = True
        script.save()
