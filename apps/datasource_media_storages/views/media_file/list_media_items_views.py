#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_media_items_views.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection, DataSourceMediaStorageItem
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class MediaView_ItemList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to see media files.")
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
                    items = DataSourceMediaStorageItem.objects.filter(
                        storage_base=media_manager).order_by('-created_at')
                    paginator = Paginator(items, 5)
                    page_no = self.request.GET.get('page')
                    page_obj = paginator.get_page(page_no)
                    item_data_list = []
                    for item in page_obj:
                        item_data_list.append({'item': item, })
                    manager_data_list.append(
                        {'storage': media_manager, 'items': page_obj, 'item_data': item_data_list, }
                    )
                agent_data_list.append({'assistant': agent, 'media_storages': manager_data_list, })
            data.append({'organization': org, 'assistants': agent_data_list, })
        context['data'] = data
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to delete media files.")
            return redirect('datasource_media_storages:list_items')
        ##############################

        if 'selected_items' in request.POST:
            item_ids = request.POST.getlist('selected_items')
            items_to_be_deleted = DataSourceMediaStorageItem.objects.filter(id__in=item_ids)
            for item in items_to_be_deleted:
                if item.full_file_path is not None:
                    try:
                        pass
                    except Exception as e:
                        pass
            DataSourceMediaStorageItem.objects.filter(id__in=item_ids).delete()
            logger.info(f"Selected media files deleted: {item_ids}")
            messages.success(request, 'Selected media files deleted successfully.')
        return redirect('datasource_media_storages:list_items')
