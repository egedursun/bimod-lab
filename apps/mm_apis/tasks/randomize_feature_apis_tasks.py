#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: randomize_feature_apis_tasks.py
#  Last Modified: 2024-09-28 16:08:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:59:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from celery import shared_task

from apps.mm_apis.models import CustomAPI
from apps.mm_apis.utils import NUMBER_OF_RANDOM_FEATURED_APIS


@shared_task
def randomize_featured_apis():
    # first switch all API's is_featured field to false
    all_apis = CustomAPI.objects.all()
    for api in all_apis:
        api.is_featured = False
        api.save()

    # then select 5 random APIs and set the is_featured field to true
    featured_apis = CustomAPI.objects.order_by('?')[:NUMBER_OF_RANDOM_FEATURED_APIS]
    for api in featured_apis:
        api.is_featured = True
        api.save()
