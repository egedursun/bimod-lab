#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: update_lean_assistant_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.leanmod.models import LeanAssistant, ExpertNetwork
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class LeanModAssistantView_Update(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        agent_id = kwargs.get('pk')
        context['lean_assistant'] = LeanAssistant.objects.get(id=agent_id)
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        context['llm_models'] = LLMCore.objects.filter(organization__users__in=[self.request.user])
        context['expert_networks'] = ExpertNetwork.objects.filter(organization__in=context['organizations'])
        context['selected_expert_networks'] = context['lean_assistant'].expert_networks.all().values_list('id',flat=True)
        return context

    def post(self, request, *args, **kwargs):
        agent_id = kwargs.get('pk')
        leanmod_agent = LeanAssistant.objects.get(id=agent_id)

        ##############################
        # PERMISSION CHECK FOR - UPDATE_LEAN_ASSISTANT
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_LEAN_ASSISTANT):
            messages.error(self.request, "You do not have permission to update LeanMod assistants.")
            return redirect('leanmod:list')
        ##############################

        org_id = request.POST.get('organization')
        llm_id = request.POST.get('llm_model')
        name = request.POST.get('name')
        instructions = request.POST.get('instructions')
        nw_ids = request.POST.getlist('expert_networks')
        agent_img = request.FILES.get('lean_assistant_image', None)
        if not org_id or not llm_id or not name or not instructions:
            messages.error(request, "Please fill in all required fields.")
            return redirect('leanmod:update', pk=agent_id)

        try:
            leanmod_agent.organization = Organization.objects.get(id=org_id)
            leanmod_agent.llm_model = LLMCore.objects.get(id=llm_id)
            leanmod_agent.name = name
            leanmod_agent.instructions = instructions
            if agent_img:
                leanmod_agent.lean_assistant_image = agent_img

            leanmod_agent.expert_networks.clear()
            if nw_ids:
                for expert_network_id in nw_ids:
                    expert_network = ExpertNetwork.objects.get(id=expert_network_id)
                    leanmod_agent.expert_networks.add(expert_network)

            leanmod_agent.save()
            messages.success(request, "Lean Assistant updated successfully.")
            return redirect('leanmod:list')
        except Exception as e:
            messages.error(request, f"Error updating Lean Assistant: {e}")
            return redirect('leanmod:update', pk=agent_id)
