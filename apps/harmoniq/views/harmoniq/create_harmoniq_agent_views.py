#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: create_harmoniq_agent_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
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
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.harmoniq.models import Harmoniq
from apps.harmoniq.utils import HARMONIQ_DEITIES
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class HarmoniqView_Create(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        context['llm_models'] = LLMCore.objects.filter(organization__in=context['organizations'])
        context['harmoniq_deities'] = HARMONIQ_DEITIES
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_HARMONIQ_AGENTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_HARMONIQ_AGENTS):
            messages.error(self.request, "You do not have permission to add Harmoniq Agents.")
            return redirect('harmoniq:list')
        ##############################

        org = request.POST.get('organization')
        llm_model = request.POST.get('llm_model')
        name = request.POST.get('name')
        desc = request.POST.get('description')
        harmoniq_deity = request.POST.get('harmoniq_deity')
        optional_instructions = request.POST.get('optional_instructions')
        if org and llm_model and name and desc and harmoniq_deity:
            harmoniq_agent = Harmoniq.objects.create(
                organization_id=org, llm_model_id=llm_model, name=name, description=desc,
                harmoniq_deity=harmoniq_deity, optional_instructions=optional_instructions,
                created_by_user=request.user
            )
            harmoniq_agent.save()
            messages.success(request, "Harmoniq Agent created successfully.")
            return redirect('harmoniq:list')
        else:
            messages.error(request, "All required fields must be filled.")
            return self.get(request, *args, **kwargs)
