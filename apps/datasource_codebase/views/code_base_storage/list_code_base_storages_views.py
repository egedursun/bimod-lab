#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: list_code_base_storages_views.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_codebase.models import CodeRepositoryStorageConnection
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CodeBaseStorageListView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_CODE_BASE
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_CODE_BASE):
            messages.error(self.request, "You do not have permission to list code base storages.")
            return context
        ##############################

        context_user = self.request.user
        user_organizations = Organization.objects.filter(users__in=[context_user])

        connections_by_organization = {}
        for organization in user_organizations:
            assistants = organization.assistants.all()
            assistants_connections = {}
            for assistant in assistants:
                connections = CodeRepositoryStorageConnection.objects.filter(assistant=assistant)
                if connections.exists():
                    assistants_connections[assistant] = connections
            if assistants_connections:
                connections_by_organization[organization] = assistants_connections

        context['connections_by_organization'] = connections_by_organization
        context['user'] = context_user
        return context
