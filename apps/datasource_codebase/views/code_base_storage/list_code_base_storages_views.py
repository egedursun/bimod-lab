#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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

from apps.datasource_codebase.models import (
    CodeRepositoryStorageConnection
)

from apps.organization.models import (
    Organization
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class CodeBaseView_StorageList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        ############################
        # Permission check
        ############################
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_CODE_BASE
        ):
            messages.error(self.request, "You do not have permission to list code base storages.")
            return context
        ############################

        try:
            user_orgs = Organization.objects.filter(
                users__in=[context_user]
            )

            conns_by_orgs = {}

            for org in user_orgs:

                conns_by_orgs[org] = {}

                for agent in org.assistants.all():
                    conns_by_orgs[org][agent] = []

            for org in user_orgs:

                for agent in org.assistants.all():

                    conns = CodeRepositoryStorageConnection.objects.filter(
                        assistant=agent
                    )

                    if conns.exists():
                        conns_by_orgs[org][agent].extend(conns)

            context['connections_by_organization'] = conns_by_orgs
            logger.info(f"[CodeBaseView_StorageList] User: {context_user} listed code base storages.")

        except Exception as e:
            logger.error(f"User: {context_user} - Code Base Storage - List Error: {e}")
            messages.error(self.request, 'An error occurred while listing Code Base Storages.')

            return context

        context['user'] = context_user

        return context
