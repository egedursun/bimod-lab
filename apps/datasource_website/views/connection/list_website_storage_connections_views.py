#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_website_storage_connections_views.py
#  Last Modified: 2024-12-07 19:39:55
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 19:39:55
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.views.generic import TemplateView

from apps.assistants.models import Assistant

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout


class DataSourceWebsiteView_StorageList(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_WEBSITE_STORAGES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.LIST_WEBSITE_STORAGES
        ):
            messages.error(self.request, "You do not have permission to list website storage connections.")
            return context
        ##############################

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        """
            {
                org1(object): {
                    assistant1(object): [datasourcewebsitestorageconnection1(object), ...],
                    ...
                },
                org2(object): {
                    assistant1(object): [datasourcewebsitestorageconnection1(object), ...],
                    ...
                },
                ...
            }
        """

        data_obj = {}

        for org in user_orgs:

            org: Organization

            data_obj[org] = {}

            for assistant in org.assistants.all():
                assistant: Assistant

                data_obj[org][assistant] = assistant.datasourcewebsitestorageconnection_set.all()

            pass

        pass

        context['data_obj'] = data_obj

        return context
