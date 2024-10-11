#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: update_expert_network_views.py
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
from apps.assistants.models import Assistant
from apps.leanmod.models import ExpertNetwork, ExpertNetworkAssistantReference
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ExpertNetworkView_Update(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        nw_id = kwargs.get('pk')
        nw = ExpertNetwork.objects.get(id=nw_id)
        agents = Assistant.objects.filter(organization__users__in=[user])
        agent_refs = nw.assistant_references.all().values('assistant_id', 'assistant__name', 'context_instructions')
        context['expert_network'] = nw
        context['assistants'] = agents
        context['assistant_references'] = [
            {
                'id': ref['assistant_id'],
                'name': ref['assistant__name'],
                'context_instructions': ref['context_instructions']
            } for ref in agent_refs ]
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_EXPERT_NETWORKS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_EXPERT_NETWORKS):
            messages.error(self.request, "You do not have permission to update Expert Network.")
            return redirect('leanmod:list_expert_networks')
        ##############################

        user = self.request.user
        nw_id = kwargs.get('pk')
        nw = ExpertNetwork.objects.get(id=nw_id)
        nw.name = request.POST.get("network_name")
        nw.meta_description = request.POST.get("network_description")
        nw.save()
        nw.assistant_references.clear()
        selected_agent_ids = request.POST.getlist("assistants")
        for agent_id in selected_agent_ids:
            agent = Assistant.objects.get(id=agent_id)
            nw_instructions = request.POST.get(f"context_instructions_{agent_id}")
            reff, created = ExpertNetworkAssistantReference.objects.get_or_create(
                network=nw, assistant=agent, defaults={
                    'context_instructions': nw_instructions, 'created_by_user': request.user,
                    'last_updated_by_user': request.user})
            if not created:
                reff.context_instructions = nw_instructions
                reff.last_updated_by_user = request.user
                reff.save()
            nw.assistant_references.add(reff)
        messages.success(request, "Expert Network updated successfully.")
        return redirect('leanmod:update_expert_network', pk=nw_id)
