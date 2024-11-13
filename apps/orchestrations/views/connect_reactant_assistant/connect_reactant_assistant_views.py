#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: connect_reactant_assistant_views.py
#  Last Modified: 2024-11-13 04:34:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 04:34:09
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
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.orchestrations.models import Maestro, OrchestrationReactantAssistantConnection
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class OrchestrationView_ConnectReactantAssistantToOrchestration(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_orgs = Organization.objects.filter(users__in=[self.request.user]).all()
        assistants = Assistant.objects.filter(organization__in=user_orgs).all()
        orchestration_maestros = Maestro.objects.filter(organization__in=user_orgs).all()
        context["assistants"] = assistants
        context["orchestration_maestros"] = orchestration_maestros
        context["existing_connections"] = OrchestrationReactantAssistantConnection.objects.filter(assistant__organization__in=user_orgs).all()
        return context

    def post(self, request, *args, **kwargs):
        assistant_id = self.request.POST.get("assistant_id")
        maestro_instance_id = self.request.POST.get("maestro_instance_id")

        ##############################
        # PERMISSION CHECK FOR - CONNECT_REACTANT_ASSISTANTS_TO_ORCHESTRATION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CONNECT_REACTANT_ASSISTANTS_TO_ORCHESTRATION):
            messages.error(self.request, "You do not have permission to connect reactant assistants to an orchestration.")
            return self.render_to_response(self.get_context_data())
        ##############################

        assistant = Assistant.objects.get(id=assistant_id)
        maestro_instance = Maestro.objects.get(id=maestro_instance_id)

        try:
            OrchestrationReactantAssistantConnection.objects.create(
                assistant=assistant,
                orchestration_maestro=maestro_instance,
                created_by_user=self.request.user
            )
        except Exception as e:
            messages.error(self.request, f"Error while connecting reactant assistant to Orchestration Maestro: {e}")
            logger.error(f"Error while connecting reactant assistant to Orchestration Maestro: {e}")

        messages.success(self.request, "Reactant assistant connected to Orchestration Maestro successfully.")
        return self.render_to_response(self.get_context_data())

