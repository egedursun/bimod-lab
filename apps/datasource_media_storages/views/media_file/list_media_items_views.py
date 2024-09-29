#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: list_media_items_views.py
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
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection, DataSourceMediaStorageItem
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceMediaStorageItemListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of media storage items associated with the user's media storage connections.

    This view retrieves all media items within the user's media storage connections, organized by organization and assistant. It also allows users to delete selected media items.

    Methods:
        get_context_data(self, **kwargs): Retrieves the media storage items for the user's connections and adds them to the context, including pagination and status information.
        post(self, request, *args, **kwargs): Handles the deletion of selected media items.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to see media files.")
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
                    items = DataSourceMediaStorageItem.objects.filter(storage_base=storage).order_by('-created_at')
                    paginator = Paginator(items, 5)  # 5 items per page
                    page_number = self.request.GET.get('page')
                    page_obj = paginator.get_page(page_number)

                    item_data_list = []
                    for item in page_obj:
                        item_data_list.append({'item': item, })
                    storage_data_list.append({'storage': storage, 'items': page_obj, 'item_data': item_data_list, })
                assistant_data_list.append({'assistant': assistant, 'media_storages': storage_data_list, })
            data.append({'organization': org, 'assistants': assistant_data_list, })
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
                        print(f"Error deleting the file from the media storage path: {item.full_file_path} // {e}")
            DataSourceMediaStorageItem.objects.filter(id__in=item_ids).delete()
            messages.success(request, 'Selected media files deleted successfully.')
            print('[DataSourceMediaStorageItemListView.post] Selected media files deleted successfully.')
        return redirect('datasource_media_storages:list_items')
