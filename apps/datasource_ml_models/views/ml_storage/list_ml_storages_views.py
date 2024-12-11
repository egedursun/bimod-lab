#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_ml_storages_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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

from django.views.generic import (
    TemplateView
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_ml_models.models import (
    DataSourceMLModelConnection
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class MLModelView_ManagerList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        ############################
        # Permission check
        ############################
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_ML_MODEL_CONNECTIONS
        ):
            messages.error(self.request, "You do not have permission to list ML Model Connections.")
            return context
        ############################

        try:
            user_orgs = context_user.organizations.all()

            mgrs_by_orgs = {}

            for org in user_orgs:
                mgrs_by_orgs[org] = {}

                for agent in org.assistants.all():
                    mgrs_by_orgs[org][agent] = []

            mgrs = DataSourceMLModelConnection.objects.filter(
                assistant__organization__in=user_orgs
            ).select_related('assistant', 'assistant__organization')

            for manager in mgrs:
                org = manager.assistant.organization
                agent = manager.assistant
                mgrs_by_orgs[org][agent].append(manager)

            context['connections_by_organization'] = mgrs_by_orgs
            logger.info("ML Model Connections were listed.")

        except Exception as e:
            logger.error(f"User: {context_user} - ML Model Connection - List Error: {e}")
            messages.error(self.request, 'An error occurred while listing ML Model Connections.')

            return context

        return context
