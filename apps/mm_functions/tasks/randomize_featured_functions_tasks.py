#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: randomize_featured_functions_tasks.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from celery import shared_task

from apps.mm_functions.models import CustomFunction
from apps.mm_functions.utils import NUMBER_OF_RANDOM_FEATURED_FUNCTIONS


logger = logging.getLogger(__name__)


@shared_task
def randomize_featured_functions():
    all_functions = CustomFunction.objects.all()
    for function in all_functions:
        function.is_featured = False
        function.save()
    featured_functions = CustomFunction.objects.order_by('?')[:NUMBER_OF_RANDOM_FEATURED_FUNCTIONS]
    for function in featured_functions:
        function.is_featured = True
        logger.info(f"Function: {function.id} is now featured.")
        function.save()
