#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: list_media_storages_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:47:09
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceListMediaStorageConnectionsView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of media storage connections associated with the user's organizations and assistants.

    This view retrieves all media storage connections organized by organization and assistant, and displays them in a structured list.

    Methods:
        get_context_data(self, **kwargs): Retrieves the media storage connections organized by organization and assistant, and adds them to the context.
        post(self, request, *args, **kwargs): Handles the deletion of selected media storage connections.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_MEDIA_STORAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_MEDIA_STORAGES):
            messages.error(self.request, "You do not have permission to list media storages.")
            return context
        ##############################

        organizations = Organization.objects.filter(users__in=[self.request.user])
        data = []
        for org in organizations:
            assistants = Assistant.objects.filter(organization=org)
            assistant_data_list = []
            for assistant in assistants:
                media_storages = DataSourceMediaStorageConnection.objects.filter(assistant=assistant)
                storage_data_list = []
                for storage in media_storages:
                    storage_data_list.append({'storage': storage})
                assistant_data_list.append({'assistant': assistant, 'media_storages': storage_data_list})
            data.append({'organization': org, 'assistants': assistant_data_list})
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

        storage_ids = request.POST.getlist('selected_storages')
        if storage_ids:
            DataSourceMediaStorageConnection.objects.filter(id__in=storage_ids).delete()
            messages.success(request, 'Selected storage connections deleted successfully.')
        return redirect('datasource_media_storages:list')
