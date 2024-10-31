#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: compile_ellma_script_views.py
#  Last Modified: 2024-10-30 17:41:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 17:41:14
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.views import View

from apps.core.ellma.ellma_execution_manager import EllmaExecutionManager
from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE, ChatRoles
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.ellma.models import EllmaScript
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames
from apps.user_permissions.utils import PermissionNames


logger = logging.getLogger(__name__)


class EllmaScriptView_CompileScript(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        script_id = kwargs.get('pk')
        ellma_transcription_language = request.POST.get('transcription_language')
        ellma_script_content = request.POST.get('script_content')

        script: EllmaScript = EllmaScript.objects.get(id=script_id)
        if not script:
            messages.error(request, "Script not found.")
            logger.error(f"[eLLMa Compilation View] Script not found.")
            return redirect('ellma:manage-scripts')

        ##############################
        # PERMISSION CHECK FOR - UPDATE_ELLMA_SCRIPTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_ELLMA_SCRIPTS):
            messages.error(self.request, "You do not have permission to update eLLMa scripts.")
            return redirect('ellma:script-editor', pk=script_id)
        ##############################

        try:
            # Do not save, since save operation is different
            ellma_script = EllmaScript.objects.get(id=script_id)
            xc = EllmaExecutionManager(script=ellma_script)
            generated_code_output, error = xc.transcribe_via_ai()
            if error:
                logger.error(f"[eLLMa Compilation View] An error occurred during compilation: {error}")
                messages.error(request, f"An error occurred during compilation: {error}")
                return redirect('ellma:script-editor', pk=script_id)
            else:
                print("Generated Code Output: ", generated_code_output)

        except ObjectDoesNotExist:
            messages.error(request, "Script not found.")
            logger.error(f"[eLLMa Compilation View] Script not found.")
            return redirect('ellma:manage-scripts')
        except Exception as e:
            messages.error(request, f"An error occurred during compilation: {str(e)}")
            logger.error(f"[eLLMa Compilation View] An error occurred during compilation: {str(e)}")
            return redirect('ellma:script-editor', pk=script_id)

        # Save the output generation as text
        script.ellma_transcribed_content = generated_code_output
        script.save()
        logger.info(f"[eLLMa Compilation View] Compiled eLLMa Script: {script.script_name}")

        try:
            tx = LLMTransaction(
                organization=script.organization, model=script.llm_model,
                responsible_user=script.created_by_user, responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, llm_cost=InternalServiceCosts.EllmaScripting.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.ELLMA_SCRIPTING, is_tool_cost=True
            )
            tx.save()
            logger.info(f"[eLLMa Compilation View] Created LLMTransaction for eLLMa Scripting Compilation Tool.")
        except Exception as e:
            logger.error(
                f"[eLLMa Compilation View] Error creating LLMTransaction for eLLMa Scripting Compilation Tool. Error: {e}")
            pass

        logger.info(f"[eLLMa Compilation View] Compiled eLLMa Script: {script.script_name}")
        return redirect('ellma:script-editor', pk=script_id)
