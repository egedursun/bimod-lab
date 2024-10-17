#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_sql_databases_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_sql.models import SQLDatabaseConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class SQLDatabaseView_ManagerList(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_SQL_DATABASES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_SQL_DATABASES):
            messages.error(self.request, "You do not have permission to list SQL Data Sources.")
            return context
        ##############################

        context_user = self.request.user
        c = SQLDatabaseConnection.objects.filter(assistant__in=Assistant.objects.filter(
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
        logger.info(f"SQL Database Connections were listed.")
        return context
