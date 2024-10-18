#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: trigger_activate_hadron_node_views.py
#  Last Modified: 2024-10-17 22:54:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:54:19
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

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.hadron_prime.models import HadronNode, HadronNodeExecutionLog
from apps.hadron_prime.utils import HadronNodeExecutionStatusesNames

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class HadronPrimeView_TriggerActiveHadronNode(View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            api_key = request.headers.get('Authorization', None)
            if not api_key:
                return JsonResponse({"success": False, "error": "API key is missing from the request. Make sure to "
                                                                "provide the HTTP header 'Authorization' with the "
                                                                "API key."})
            if "Bearer" in api_key:
                api_key = (api_key.replace("Bearer ", "").replace("bearer ", "").replace("BEARER ", "")
                           .replace("Bearer", "").replace("bearer", "").replace("BEARER", ""))
                logger.info("Format of the API key is fixed to remove Bearer prefix.")
            else:
                logger.info("API key format is already correct, no fix applied.")

            node = get_object_or_404(HadronNode, id=kwargs['pk'])
            if api_key != node.activation_trigger_authentication_key:
                return JsonResponse({"success": False, "error": "Invalid API key provided."})

            xc_log = HadronNodeExecutionLog.objects.create(
                node=node, execution_log=None, execution_status=HadronNodeExecutionStatusesNames.PENDING,
                created_at=timezone.now())

            # TODO: Implement node activation service
            pass

            return JsonResponse({"success": True, "error": None})

        except Exception as e:
            return JsonResponse({"success": False, "error": f"Internal Server Error: {str(e)}"})
