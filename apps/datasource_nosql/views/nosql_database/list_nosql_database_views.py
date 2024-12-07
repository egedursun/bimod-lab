#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.assistants.models import Assistant

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_nosql.models import (
    NoSQLDatabaseConnection
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class NoSQLDatabaseView_ManagerList(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        ##############################
        # Permission check
        ##############################
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_NOSQL_DATABASES
        ):
            messages.error(self.request, "You do not have permission to list NoSQL Data Sources.")
            return context
        ##############################

        try:
            c_by_orgs = {}
            user_orgs = context_user.organizations.all()

            for org in user_orgs:
                c_by_orgs[org] = {}
                for assistant in org.assistants.all():
                    c_by_orgs[org][assistant] = []

            connections = NoSQLDatabaseConnection.objects.filter(
                assistant__organization__in=user_orgs
            ).select_related('assistant', 'assistant__organization')

            for connection in connections:
                org = connection.assistant.organization
                assistant = connection.assistant
                c_by_orgs[org][assistant].append(connection)

            context['connections_by_organization'] = c_by_orgs
            logger.info("NoSQL Database Connections were listed.")

        except Exception as e:
            logger.error(f"User: {context_user} - NoSQL Data Source - List Error: {e}")
            messages.error(self.request, 'An error occurred while listing NoSQL Data Sources.')

            return context

        return context
