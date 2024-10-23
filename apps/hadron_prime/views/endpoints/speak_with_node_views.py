#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: speak_with_system_views.py
#  Last Modified: 2024-10-22 13:56:36
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 13:56:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import json
import logging

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.core.hadron_prime.hadron_prime_executor import HadronPrimeExecutor
from apps.hadron_prime.models import HadronNode

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class HadronPrimeView_SpeakWithHadronNode(View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            api_key = request.headers.get('Authorization', None)
            if not api_key:
                return JsonResponse({
                    "success": False,
                    "error": "API key is missing from the request. Make sure to provide the HTTP header 'Authorization' with the API key.",
                    "data": {}
                })
            if "Bearer" in api_key:
                api_key = (api_key.replace("Bearer ", "").replace("bearer ", "").replace("BEARER ", "")
                           .replace("Bearer", "").replace("bearer", "").replace("BEARER", ""))
                logger.info("Format of the API key is fixed to remove Bearer prefix.")
            else:
                logger.info("API key format is already correct, no fix applied.")

            node = get_object_or_404(HadronNode, id=kwargs['pk'])
            if api_key != node.activation_trigger_authentication_key:
                return JsonResponse({
                    "success": False,
                    "error": "Invalid API key provided.",
                    "data": {}
                })

            try:
                request_body = json.loads(request.body.decode('utf-8'))
            except Exception as e:
                return JsonResponse({
                    "success": False,
                    "error": f"Error parsing request body: {str(e)}",
                    "data": {}
                })

            user_query_text = request_body.get('user_query_text', None)
            if not user_query_text or user_query_text == "":
                return JsonResponse({
                    "success": False,
                    "error": "User query text is missing from the request.",
                    "data": {}
                })

            xc = HadronPrimeExecutor(node=node, execution_log_object=None)
            response_text, success, error = xc.generate_node_speech(user_query_text=user_query_text)
            if error:
                logger.error(f"Error occurred while generating speech for the Hadron Node: {error}")
                return JsonResponse({
                    "success": False,
                    "error": error,
                    "data": {}
                })

            logger.info(f"Hadron Node speech generation completed with status: {success}")
            return JsonResponse({
                "success": success,
                "error": error,
                "data": {
                    "response": response_text
                }
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": f"Internal Server Error: {str(e)}",
                "data": {}
            })


class HadronPrimeView_SpeakWithHadronNodeViaForm(View):
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

            user_query_text = request.POST.get('user_query_text', None)
            if not user_query_text or user_query_text == "":
                messages.error(request, "User query text is missing from the request.")
                return redirect('hadron_prime:detail_hadron_node', pk=node_id)

            xc = HadronPrimeExecutor(node=node, execution_log_object=None)
            _, success, error = xc.generate_node_speech(user_query_text=user_query_text)
            if error:
                logger.error(f"Error occurred while generating speech for the Hadron Node: {error}")
                messages.error(request, f"Error occurred while generating speech for the Hadron Node: {error}")
                return redirect('hadron_prime:detail_hadron_node', pk=node_id)

            logger.info(f"Hadron Node speech generation completed with status: {success}")
            messages.success(request, "Hadron Node speech generation completed successfully.")
            return redirect('hadron_prime:detail_hadron_node', pk=node_id)

        except Exception as e:
            messages.error(request, f"Internal Server Error: {str(e)}")
            return redirect('hadron_prime:detail_hadron_node', pk=node_id)
