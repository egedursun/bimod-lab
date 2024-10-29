#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_screenshot_delivery_views.py
#  Last Modified: 2024-10-28 20:39:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:39:28
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class MetaTempoView_ScreenshotDelivery(View):

    # TODO-EGE: Functional view, the screenshots will be delivered to our server here, and then 'executor' in 'core'
    #       will be called to save the element (log).

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass
