#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: list_assistants_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:19:01
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
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListAssistantView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of assistants associated with the user's organizations.

    This view retrieves all assistants that belong to the organizations the user is a part of and displays them in a list. Currently, all authenticated users are allowed to view the list of assistants.

    Methods:
        get_context_data(self, **kwargs): Retrieves the assistants for the user's organizations and adds them to the context.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - LIST_ASSISTANTS
        if not UserPermissionManager.is_authorized(user=user, operation=PermissionNames.LIST_ASSISTANTS):
            messages.error(self.request, "You do not have permission to list assistants.")
            return context
        ##############################

        organizations = Organization.objects.filter(users__in=[user])
        org_assistants = {org: org.assistants.all() for org in organizations}
        context['org_assistants'] = org_assistants
        return context
