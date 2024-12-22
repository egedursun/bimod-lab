#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: store_knowledge_bases_list_views.py
#  Last Modified: 2024-12-21 19:06:25
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-21 19:06:25
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.views.generic import (
    TemplateView
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_knowledge_base.models import (
    DocumentKnowledgeBaseConnection
)

from apps.knowledge_base_store.models import (
    KnowledgeBaseIntegration
)

from apps.knowledge_base_store.utils import (
    KNOWLEDGE_BASE_CATEGORIES
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import (
    TemplateLayout
)


class KnowledgeBaseStoreView_StoreKnowledgeBaseList(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_KNOWLEDGE_BASE_INTEGRATIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_KNOWLEDGE_BASE_INTEGRATIONS
        ):
            messages.error(self.request, "You do not have permission to list Knowledge Base Integrations.")
            return context
        ##############################

        all_knowledge_base_integrations = KnowledgeBaseIntegration.objects.all()

        category_groups = defaultdict(list)

        for knowledge_base_integration in all_knowledge_base_integrations:
            category_groups[
                knowledge_base_integration.get_knowledge_base_category_display()
            ].append(
                knowledge_base_integration
            )

        complete_categories = KNOWLEDGE_BASE_CATEGORIES

        for complete_category, category_label in complete_categories:
            if category_label not in category_groups:
                category_groups[category_label] = []

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        knowledge_base_store_connections = DocumentKnowledgeBaseConnection.objects.filter(
            assistant__organization__in=user_orgs
        )

        context['category_groups'] = dict(category_groups)
        context['knowledge_base_store_connections'] = knowledge_base_store_connections

        return context

        return context
