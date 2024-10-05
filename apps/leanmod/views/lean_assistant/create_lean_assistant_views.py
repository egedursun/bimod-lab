#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: create_lean_assistant_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:31
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: create_lean_assistant_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:55:30
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.leanmod.models import ExpertNetwork, LeanAssistant
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateLeanAssistantView(LoginRequiredMixin, TemplateView):
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
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_LEAN_ASSISTANT
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_LEAN_ASSISTANT):
            messages.error(self.request, "You do not have permission to add new LeanMod assistants.")
            return redirect('leanmod:list')
        ##############################

        # Fetch form data
        organization_id = request.POST.get('organization')
        llm_model_id = request.POST.get('llm_model')
        name = request.POST.get('name')
        instructions = request.POST.get('instructions')
        expert_network_ids = request.POST.getlist('expert_networks')
        lean_assistant_image = request.FILES.get('lean_assistant_image')

        # Validate required fields
        if not organization_id or not llm_model_id or not name or not instructions:
            messages.error(request, "Please fill in all required fields.")
            return redirect('leanmod:create')

        try:
            # Create new Lean Assistant
            organization = Organization.objects.get(id=organization_id)
            llm_model = LLMCore.objects.get(id=llm_model_id)
            lean_assistant = LeanAssistant.objects.create(
                organization=organization,
                llm_model=llm_model,
                name=name,
                instructions=instructions,
                lean_assistant_image=lean_assistant_image,
                created_by_user=request.user,
                last_updated_by_user=request.user,
            )

            # Add expert networks if selected
            if expert_network_ids:
                for expert_network_id in expert_network_ids:
                    expert_network = ExpertNetwork.objects.get(id=expert_network_id)
                    lean_assistant.expert_networks.add(expert_network)

            lean_assistant.save()
            messages.success(request, "Lean Assistant created successfully.")
            return redirect('leanmod:list')

        except Exception as e:
            messages.error(request, f"Error creating Lean Assistant: {e}")
            return redirect('leanmod:create')
