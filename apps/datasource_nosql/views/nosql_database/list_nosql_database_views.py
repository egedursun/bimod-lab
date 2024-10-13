#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: list_nosql_database_views.py
#  Last Modified: 2024-10-12 13:21:24
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 13:21:25
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_nosql.models import NoSQLDatabaseConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class NoSQLDatabaseView_ManagerList(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_NOSQL_DATABASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_NOSQL_DATABASES):
            messages.error(self.request, "You do not have permission to list NoSQL Data Sources.")
            return context
        ##############################

        context_user = self.request.user
        c = NoSQLDatabaseConnection.objects.filter(assistant__in=Assistant.objects.filter(
            organization__in=context_user.organizations.all())).select_related('assistant__organization')

        c_by_orgs = {}
        for connection in c:
            orgs = connection.assistant.organization
            agent = connection.assistant
            if orgs not in c_by_orgs:
                c_by_orgs[orgs] = {}
            if agent not in c_by_orgs[orgs]:
                c_by_orgs[orgs][agent] = []
            c_by_orgs[orgs][agent].append(connection)
        context['connections_by_organization'] = c_by_orgs
        return context
