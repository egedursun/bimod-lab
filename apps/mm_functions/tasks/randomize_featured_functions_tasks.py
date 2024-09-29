#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: randomize_featured_functions_tasks.py
#  Last Modified: 2024-09-28 16:27:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:01:13
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from celery import shared_task

from apps.mm_functions.models import CustomFunction
from apps.mm_functions.utils import NUMBER_OF_RANDOM_FEATURED_FUNCTIONS


@shared_task
def randomize_featured_functions():
    # first switch all function's is_featured field to false¬
    all_functions = CustomFunction.objects.all()
    for function in all_functions:
        function.is_featured = False
        function.save()
    # then select 5 random functions and set the is_featured field to true
    featured_functions = CustomFunction.objects.order_by('?')[:NUMBER_OF_RANDOM_FEATURED_FUNCTIONS]
    for function in featured_functions:
        function.is_featured = True
        function.save()
