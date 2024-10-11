#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: list_media_storages_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:48
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
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class MediaView_ManagerList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_MEDIA_STORAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_MEDIA_STORAGES):
            messages.error(self.request, "You do not have permission to list media storages.")
            return context
        ##############################

        orgs = Organization.objects.filter(users__in=[self.request.user])
        data = []
        for org in orgs:
            agents = Assistant.objects.filter(organization=org)
            agent_data_list = []
            for agent in agents:
                media_managers = DataSourceMediaStorageConnection.objects.filter(assistant=agent)
                manager_data_list = []
                for media_manager in media_managers:
                    manager_data_list.append({'storage': media_manager})
                agent_data_list.append({'assistant': agent, 'media_storages': manager_data_list})
            data.append({'organization': org, 'assistants': agent_data_list})
        context['data'] = data
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_MEDIA_STORAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_MEDIA_STORAGES):
            messages.error(self.request, "You do not have permission to delete media storages.")
            return redirect('datasource_media_storages:list')
        ##############################

        mm_ids = request.POST.getlist('selected_storages')
        if mm_ids:
            DataSourceMediaStorageConnection.objects.filter(id__in=mm_ids).delete()
            messages.success(request, 'Selected storage connections deleted successfully.')
        return redirect('datasource_media_storages:list')
