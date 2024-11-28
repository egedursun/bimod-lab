#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: pwa_service_views.py
#  Last Modified: 2024-11-28 00:59:35
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-28 00:59:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def service_worker(request):
    try:
        with open('src/assets/pwa/service-worker.js', 'r') as f:
            js_code = f.read()
    except FileNotFoundError:
        return HttpResponse("Service Worker not found.", status=404)
    response = HttpResponse(js_code, content_type='application/javascript')
    response['Service-Worker-Allowed'] = '/app/mobile_client/'
    return response
