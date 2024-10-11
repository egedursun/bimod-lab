#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_all_llm_models_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.llm_core.models import LLMCore
from apps.user_permissions.utils import PermissionNames


class SettingsView_DeleteAllLLMModels(View, LoginRequiredMixin):

    def post(self, request, *args, **kwargs):
        user = request.user
        user_llm_models = LLMCore.objects.filter(organization__users__in=[user]).all()
        confirmation_field = request.POST.get('confirmation', None)
        if confirmation_field != 'CONFIRM DELETING ALL LLM MODELS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL LLM MODELS'.")
            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_LLM_CORES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_LLM_CORES):
            messages.error(self.request, "You do not have permission to delete LLM models.")
            return redirect('user_settings:settings')
        ##############################

        try:
            for llm_model in user_llm_models:
                llm_model.delete()
            messages.success(request, "All LLM models associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting LLM models: {e}")
        return redirect('user_settings:settings')
