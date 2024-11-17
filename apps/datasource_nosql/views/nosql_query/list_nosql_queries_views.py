#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_nosql_queries_views.py
#  Last Modified: 2024-10-12 13:22:24
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 13:22:25
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
from apps.datasource_nosql.models import CustomNoSQLQuery
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class NoSQLDatabaseView_QueryList(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_CUSTOM_NOSQL_QUERIES
        if not UserPermissionManager.is_authorized(
            user=self.request.user, operation=PermissionNames.LIST_CUSTOM_NOSQL_QUERIES):
            messages.error(self.request, "You do not have permission to list custom NoSQL queries.")
            return context
        ##############################

        context_user = self.request.user
        queries = CustomNoSQLQuery.objects.filter(
            database_connection__assistant__in=Assistant.objects.filter(
                organization__in=context_user.organizations.all())).select_related(
            'database_connection__assistant', 'database_connection__assistant__organization')

        try:
            queries_by_orgs = {}
            for qu in queries:
                org = qu.database_connection.assistant.organization
                agent = qu.database_connection.assistant
                if org not in queries_by_orgs:
                    queries_by_orgs[org] = {}
                if agent not in queries_by_orgs[org]:
                    queries_by_orgs[org][agent] = []
                queries_by_orgs[org][agent].append(qu)
        except Exception as e:
            logger.error(f"User: {context_user} - NoSQL Query - List Error: {e}")
            messages.error(self.request, 'An error occurred while listing NoSQL Queries.')
            return context

        context['queries_by_organization'] = queries_by_orgs
        logger.info(f"NoSQL Queries were listed.")
        return context
