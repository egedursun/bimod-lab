#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_ellma_script_views.py
#  Last Modified: 2024-10-30 17:38:35
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 17:38:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.ellma.models import EllmaScript
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames


class EllmaScriptView_CreateScript(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - CREATE_ELLMA_SCRIPTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_ELLMA_SCRIPTS):
            messages.error(self.request, "You do not have permission to create eLLMa scripts.")
            return redirect('ellma:manage-scripts')
        ##############################

        organization_id = request.POST.get('organization')
        llm_model_id = request.POST.get('llm_model')
        script_name = request.POST.get('script_name')
        if not all([organization_id, llm_model_id, script_name]):
            messages.error(request, "Missing required fields.")
            return redirect('ellma:manage-scripts')

        try:
            organization = Organization.objects.get(id=organization_id)
            llm_model = LLMCore.objects.get(id=llm_model_id)
        except ObjectDoesNotExist:
            messages.error(request, "Organization or LLM Model not found.")
            return redirect('ellma:manage-scripts')

        ellma_script = EllmaScript.objects.create(
            organization=organization, llm_model=llm_model, script_name=script_name, created_by_user=request.user
        )
        messages.success(request, f"Script '{ellma_script.script_name}' created successfully.")
        return redirect('ellma:manage-scripts')
