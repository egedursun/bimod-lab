#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_lean_assistants_views.py
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

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class LeanModAssistantView_List(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_LEAN_ASSISTANT
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_LEAN_ASSISTANT
        ):
            messages.error(self.request, "You do not have permission to list LeanMod assistants.")
            return context
        ##############################

        org_lean_agents = {}

        orgs = Organization.objects.prefetch_related(
            'lean_assistants'
        ).filter(
            users__in=[self.request.user]
        ).all()

        for organization in orgs:
            org_lean_agents[organization] = organization.lean_assistants.all()

        context['org_lean_assistants'] = org_lean_agents
        logger.info(f"LeanMod Assistants were listed by User: {self.request.user.id}.")

        return context
