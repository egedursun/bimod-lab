#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: list_llm_cores_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:56:26
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListLLMCoreView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of all LLM Core models associated with the user's organizations.

    This view retrieves all LLM Core models linked to the organizations that the user belongs to and displays them.

    Methods:
        get_context_data(self, **kwargs): Retrieves the LLM Core models for the user's organizations and adds them to the context.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_LLM_CORES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_LLM_CORES):
            messages.error(self.request, "You do not have permission to list LLM Cores.")
            return context
        ##############################

        user = self.request.user
        organizations = user.organizations.all()
        # retrieve the llm cores for every organization and store in the dictionary
        llm_cores = {}
        for organization in organizations:
            llm_cores[organization] = organization.llm_cores.all()
        context['organizations'] = organizations
        context['org_llm_cores'] = llm_cores
        return context
