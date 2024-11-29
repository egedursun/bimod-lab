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
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


@csrf_exempt
def service_worker(request):
    try:
        with open('src/assets/pwa/service-worker.js', 'r') as f:
            js_code = f.read()

    except FileNotFoundError:
        logger.error("Service Worker not found.")
        return HttpResponse(
            "Service Worker not found.",
            status=404
        )

    except Exception as e:
        logger.error(f"Service Worker error: {e}")

        return HttpResponse(
            "Service Worker error.",
            status=500
        )

    response = HttpResponse(
        js_code,
        content_type='application/javascript'
    )

    response['Service-Worker-Allowed'] = '/'
    return response
