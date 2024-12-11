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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_nosql.models import (
    CustomNoSQLQuery
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class NoSQLDatabaseView_QueryList(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context_user = self.request.user

        ##############################
        # Permission check
        ##############################
        if not UserPermissionManager.is_authorized(
            user=context_user,
            operation=PermissionNames.LIST_CUSTOM_NOSQL_QUERIES
        ):
            messages.error(self.request, "You do not have permission to list custom NoSQL queries.")
            return context
        ##############################

        try:
            queries_by_orgs = {}
            user_orgs = context_user.organizations.all()

            for org in user_orgs:

                queries_by_orgs[org] = {}

                for assistant in org.assistants.all():
                    queries_by_orgs[org][assistant] = []

            queries = CustomNoSQLQuery.objects.filter(
                database_connection__assistant__organization__in=user_orgs
            ).select_related(
                'database_connection__assistant',
                'database_connection__assistant__organization'
            )

            for qu in queries:
                org = qu.database_connection.assistant.organization

                assistant = qu.database_connection.assistant
                queries_by_orgs[org][assistant].append(qu)

            context['queries_by_organization'] = queries_by_orgs
            logger.info("Custom NoSQL Queries were listed.")

        except Exception as e:
            logger.error(f"User: {context_user} - NoSQL Query - List Error: {e}")
            messages.error(self.request, 'An error occurred while listing NoSQL Queries.')

            return context

        return context
