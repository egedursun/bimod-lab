#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_lean_assistant_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.assistants.utils import (
    CONTEXT_MANAGEMENT_STRATEGY,
    ContextManagementStrategyNames
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.leanmod.models import (
    ExpertNetwork,
    LeanAssistant
)

from apps.llm_core.models import LLMCore
from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class LeanModAssistantView_Create(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context['organizations'] = Organization.objects.filter(
            users__in=[self.request.user]
        )

        context['llm_models'] = LLMCore.objects.filter(
            organization__users__in=[self.request.user]
        )

        context['expert_networks'] = ExpertNetwork.objects.filter(
            organization__in=context['organizations']
        )

        context['context_overflow_strategies'] = CONTEXT_MANAGEMENT_STRATEGY

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_LEAN_ASSISTANT
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_LEAN_ASSISTANT
        ):
            messages.error(self.request, "You do not have permission to add new LeanMod assistants.")
            return redirect('leanmod:list')
        ##############################

        org_id = request.POST.get('organization')
        llm_id = request.POST.get('llm_model')
        name = request.POST.get('name')
        instructions = request.POST.get('instructions')

        nw_ids = request.POST.getlist('expert_networks')
        agent_img = request.FILES.get('lean_assistant_image')
        max_context_messages = request.POST.get('max_context_messages') or 25

        context_overflow_strategy = request.POST.get(
            'context_overflow_strategy'
        ) or ContextManagementStrategyNames.FORGET

        if (
            not org_id or
            not llm_id or
            not name or
            not instructions
        ):
            logger.error("Please fill in all required fields.")
            messages.error(request, "Please fill in all required fields.")

            return redirect('leanmod:create')

        try:
            org = Organization.objects.get(
                id=org_id
            )

            llm_model = LLMCore.objects.get(
                id=llm_id
            )

            leanmod_agent = LeanAssistant.objects.create(
                organization=org,
                llm_model=llm_model,
                name=name,
                instructions=instructions,
                max_context_messages=max_context_messages,
                context_overflow_strategy=context_overflow_strategy,
                lean_assistant_image=agent_img,
                created_by_user=request.user,
                last_updated_by_user=request.user
            )

            if nw_ids:
                for nw_id in nw_ids:
                    nw = ExpertNetwork.objects.get(
                        id=nw_id
                    )

                    leanmod_agent.expert_networks.add(nw)

            leanmod_agent.save()

            logger.info(f"Lean Assistant {leanmod_agent.name} was created by User: {self.request.user.id}.")
            messages.success(request, "Lean Assistant created successfully.")

            return redirect('leanmod:list')

        except Exception as e:
            logger.error(f"Error creating Lean Assistant: {e}")
            messages.error(request, f"Error creating Lean Assistant: {e}")

            return redirect('leanmod:create')
