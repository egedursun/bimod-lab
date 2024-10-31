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
        script: EllmaScript = EllmaScript.objects.get(id=script_id)
        if not script:
            messages.error(request, "Script not found.")
            return redirect('ellma:manage-scripts')

        ##############################
        # PERMISSION CHECK FOR - UPDATE_ELLMA_SCRIPTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_ELLMA_SCRIPTS):
            messages.error(self.request, "You do not have permission to update eLLMa scripts.")
            return redirect('ellma:script-editor', pk=script_id)
        ##############################

        try:
            ellma_script = EllmaScript.objects.get(id=script_id)
            script_content = ellma_script.ellma_script_content
            transcription_language = ellma_script.ellma_transcription_language
            if not script_content:
                messages.error(request, "The script content is empty. Please add content before compiling.")
                return redirect('ellma:script-editor', pk=script_id)

            print("LLM Operation Placeholder: Preparing to transcribe to", transcription_language)
            # TODO: Implement LLM transcription logic here.

            messages.success(request, "Script compiled successfully.")
        except ObjectDoesNotExist:
            messages.error(request, "Script not found.")
        except Exception as e:
            messages.error(request, f"An error occurred during compilation: {str(e)}")

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

        return redirect('ellma:script-editor', pk=script_id)
