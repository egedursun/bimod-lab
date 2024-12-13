#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_export_orchestrations_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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

from django.views.generic import (
    TemplateView
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.export_orchestrations.models import (
    ExportOrchestrationAPI
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from config.settings import (
    MAX_ORCHESTRATIONS_EXPORTS_ORGANIZATION
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class ExportOrchestrationView_List(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_EXPORT_ORCHESTRATION
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_EXPORT_ORCHESTRATION
        ):
            messages.error(self.request, "You do not have permission to list Export Orchestration APIs.")
            return context
        ##############################

        user_context = self.request.user
        max_exp_orchs = MAX_ORCHESTRATIONS_EXPORTS_ORGANIZATION

        try:
            org_data = []

            orgs = Organization.objects.filter(
                users=user_context
            )

            for org in orgs:
                n_exp_agents = org.exported_orchestrations.count()
                agents_pct = round((n_exp_agents / max_exp_orchs) * 100, 2)
                exp_agents = org.exported_orchestrations.all()

                for agent in exp_agents:
                    agent.usage_percentage = 100

                org_data.append(
                    {
                        'organization': org,
                        'export_assistants_count': n_exp_agents,
                        'assistants_percentage': agents_pct,
                        'export_assistants': exp_agents,
                        'limit': max_exp_orchs
                    }
                )

            exp_agents = ExportOrchestrationAPI.objects.filter(
                created_by_user=user_context
            )

            context["user"] = user_context
            context["organization_data"] = org_data
            context["export_assistants"] = exp_agents

        except Exception as e:
            messages.error(self.request, f"An error occurred: {str(e)}")

            return context

        logger.info(f"User: {user_context.id} listed Export Orchestration APIs.")

        return context
