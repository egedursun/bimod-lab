#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_expert_network_views.py
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

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.assistants.models import Assistant

from apps.leanmod.models import (
    ExpertNetwork,
    ExpertNetworkAssistantReference
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ExpertNetworkView_Create(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context['assistants'] = Assistant.objects.filter(
            organization__users__in=[user]
        )

        context['organizations'] = Organization.objects.filter(
            users__in=[user]
        )

        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_EXPERT_NETWORK
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_EXPERT_NETWORKS
        ):
            messages.error(self.request, "You do not have permission to add Expert Network.")
            return redirect('leanmod:list_expert_networks')
        ##############################

        name = request.POST.get("network_name")
        desc = request.POST.get("network_description")
        selected_agent_ids = request.POST.getlist("assistants")
        org_id = request.POST.get("organization")

        try:
            org = Organization.objects.get(
                id=org_id
            )

        except Organization.DoesNotExist:
            logger.error(f"Selected organization does not exist.")
            messages.error(request, "Selected organization does not exist.")

            return redirect('leanmod:create_expert_network')

        try:
            expert_network = ExpertNetwork.objects.create(
                name=name,
                meta_description=desc,
                organization=org,
                created_by_user=request.user,
                last_updated_by_user=request.user
            )

        except Exception as e:
            logger.error(f"Error creating Expert Network: {e}")
            messages.error(request, f"Error creating Expert Network: {e}")

            return redirect('leanmod:create_expert_network')

        for agent_id in selected_agent_ids:
            agent = Assistant.objects.get(
                id=agent_id
            )

            nw_instructions = request.POST.get(f"context_instructions_{agent_id}")

            try:
                reference = ExpertNetworkAssistantReference.objects.create(
                    network=expert_network,
                    assistant=agent,
                    context_instructions=nw_instructions,
                    created_by_user=request.user,
                    last_updated_by_user=request.user
                )

                expert_network.assistant_references.add(
                    reference
                )

                expert_network.save()

            except Exception as e:
                logger.error(f"Error creating Expert Network Assistant Reference: {e}")
                messages.error(request, f"Error creating Expert Network Assistant Reference: {e}")

                return redirect('leanmod:create_expert_network')

        logger.info(f"Expert Network created successfully with selected assistants.")
        messages.success(request, "Expert Network created successfully with selected assistants.")

        return redirect('leanmod:list_expert_networks')
