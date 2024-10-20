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

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.core.hadron_prime.hadron_prime_executor import HadronPrimeExecutor
from apps.core.hadron_prime.utils import NodeExecutionProcessLogTexts
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
            xc_log.save()
            xc_log.execution_log = ""
            xc_log.execution_log += NodeExecutionProcessLogTexts.system_initialized(node=node)
            xc_log.execution_log += NodeExecutionProcessLogTexts.topics_initialized(node=node)
            xc_log.execution_log += NodeExecutionProcessLogTexts.node_initialized(node=node)
            node.execution_logs.add(xc_log)
            node.save()

            xc = HadronPrimeExecutor(node=node, execution_log_object=xc_log)
            success, error = xc.execute_hadron_node()
            if error:
                logger.error(f"Error occurred while executing the Hadron Node: {error}")
                xc_log.execution_status = HadronNodeExecutionStatusesNames.FAILED
                xc_log.execution_log += NodeExecutionProcessLogTexts.process_failed(error_log=error)
                xc_log.save()
                return JsonResponse({"success": False, "error": error})

            logger.info(f"Hadron Node execution completed with status: {success}")
            return JsonResponse({"success": success, "error": error})

        except Exception as e:
            return JsonResponse({"success": False, "error": f"Internal Server Error: {str(e)}"})


class HadronPrimeView_TriggerActiveHadronNodeViaForm(View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        node_id = request.POST.get('node_id', None)
        id_token = request.POST.get('id_token', None)
        try:
            api_key = request.POST.get('api_key', None)
            if not api_key:
                messages.error(request, "API key is missing from the request. Make sure to provide the API key.")
                return redirect('hadron_prime:detail_hadron_node', pk=node_id)

            node = get_object_or_404(HadronNode, id=node_id)

            if id_token != node.activation_trigger_hashed_param:
                messages.error(request, "Invalid ID token provided.")
                return redirect('hadron_prime:detail_hadron_node', pk=node_id)
            if api_key != node.activation_trigger_authentication_key:
                messages.error(request, "Invalid API key provided.")
                return redirect('hadron_prime:detail_hadron_node', pk=node_id)

            xc_log = HadronNodeExecutionLog.objects.create(
                node=node, execution_log=None, execution_status=HadronNodeExecutionStatusesNames.PENDING,
                created_at=timezone.now())
            xc_log.save()
            xc_log.execution_log = ""
            xc_log.execution_log += NodeExecutionProcessLogTexts.system_initialized(node=node)
            xc_log.execution_log += NodeExecutionProcessLogTexts.topics_initialized(node=node)
            xc_log.execution_log += NodeExecutionProcessLogTexts.node_initialized(node=node)
            node.execution_logs.add(xc_log)
            node.save()

            xc = HadronPrimeExecutor(node=node, execution_log_object=xc_log)
            success, error = xc.execute_hadron_node()
            if error:
                logger.error(f"Error occurred while executing the Hadron Node: {error}")
                xc_log.execution_status = HadronNodeExecutionStatusesNames.FAILED
                xc_log.execution_log += NodeExecutionProcessLogTexts.process_failed(error_log=error)
                xc_log.save()
                messages.error(request, f"Error occurred while executing the Hadron Node: {error}")
                return redirect('hadron_prime:detail_hadron_node', pk=node_id)

            logger.info(f"Hadron Node execution completed with status: {success}")
            messages.success(request, "Hadron Node execution completed successfully.")
            return redirect('hadron_prime:detail_hadron_node', pk=node_id)

        except Exception as e:
            messages.error(request, f"Internal Server Error: {str(e)}")
            return redirect('hadron_prime:detail_hadron_node', pk=node_id)
