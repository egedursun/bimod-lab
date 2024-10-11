#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_ml_models.models import DataSourceMLModelConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class MLModelView_ManagerList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_ML_MODEL_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_ML_MODEL_CONNECTIONS):
            messages.error(self.request, "You do not have permission to list ML Model Connections.")
            return context
        ##############################

        context_user = self.request.user
        mgrs = DataSourceMLModelConnection.objects.filter(
            assistant__in=Assistant.objects.filter(organization__in=context_user.organizations.all())
        ).select_related('assistant__organization')

        mgrs_by_orgs = {}
        for manager in mgrs:
            org = manager.assistant.organization
            agent = manager.assistant
            if org not in mgrs_by_orgs:
                mgrs_by_orgs[org] = {}
            if agent not in mgrs_by_orgs[org]:
                mgrs_by_orgs[org][agent] = []
            mgrs_by_orgs[org][agent].append(manager)
        context['connections_by_organization'] = mgrs_by_orgs
        return context
