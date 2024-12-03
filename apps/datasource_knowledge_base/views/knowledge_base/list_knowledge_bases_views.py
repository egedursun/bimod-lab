#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_knowledge_bases_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:47
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

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_knowledge_base.models import (
    DocumentKnowledgeBaseConnection
)

from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class VectorStoreView_List(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_KNOWLEDGE_BASES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_KNOWLEDGE_BASES
        ):
            messages.error(self.request, "You do not have permission to list Knowledge Bases.")
            return context
        ##############################

        try:
            context_user = self.request.user
            user_orgs = Organization.objects.filter(
                users__in=[context_user]
            )

            conns_by_orgs = {}

            for org in user_orgs:
                agents = org.assistants.all()
                agents_conns = {}

                for agent in agents:
                    conn = DocumentKnowledgeBaseConnection.objects.filter(
                        assistant=agent
                    )

                    if conn.exists():
                        agents_conns[agent] = conn

                if agents_conns:
                    conns_by_orgs[org] = agents_conns

        except Exception as e:
            logger.error(f"User: {self.request.user} - Knowledge Base - List Error: {e}")
            messages.error(self.request, 'An error occurred while listing the knowledge bases.')

            return context

        context['connections_by_organization'] = conns_by_orgs
        context['user'] = context_user
        logger.info(f"Knowledge Bases were listed.")

        return context
