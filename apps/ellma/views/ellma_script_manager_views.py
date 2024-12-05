#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ellma_script_manager_views.py
#  Last Modified: 2024-10-30 17:39:02
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 17:39:02
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
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.ellma.models import EllmaScript
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class EllmaScriptView_ManageScripts(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_ELLMA_SCRIPTS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_ELLMA_SCRIPTS
        ):
            messages.error(self.request, "You do not have permission to list eLLMa scripts.")
            return context
        ##############################

        try:
            user_orgs = Organization.objects.filter(users__in=[self.request.user])
            org_scripts = {}

            for org in user_orgs:
                scripts = EllmaScript.objects.filter(organization=org)
                org_scripts[org] = scripts

            context['org_scripts'] = org_scripts
            context["organizations"] = user_orgs
            context['llm_models'] = LLMCore.objects.filter(organization__in=user_orgs)

        except Exception as e:
            messages.error(self.request, f"An error occurred: {str(e)}")
            return context

        return context
