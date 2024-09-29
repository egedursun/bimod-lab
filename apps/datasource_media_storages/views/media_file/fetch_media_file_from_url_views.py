#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: fetch_media_file_from_url_views.py
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
from apps.datasource_media_storages.tasks import download_file_from_url
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceMediaStorageItemFetchFileFromUrl(LoginRequiredMixin, TemplateView):
    """
    Fetches and uploads a file from a given URL to a selected media storage connection.

    This view allows users with the appropriate permissions to fetch and upload a file from a specified URL to a selected media storage connection.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for rendering the confirmation of the file fetch.
        post(self, request, *args, **kwargs): Handles the file fetch and upload process from the specified URL.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to add media files.")
            return redirect('datasource_media_storages:list_items')
        ##############################

        media_storage_id = request.POST.get('storage_id') or None
        if not media_storage_id:
            messages.error(request, 'Invalid media storage ID.')
            return redirect('datasource_media_storages:create_item')
        download_url = request.POST.get('download_url') or None
        if not download_url:
            messages.error(request, 'Invalid download URL.')
            return redirect('datasource_media_storages:create_item')
        media_storage_id_int = int(media_storage_id)
        download_file_from_url.delay(storage_id=media_storage_id_int, url=download_url)
        messages.success(request, 'File download from URL initiated.')
        print('[DataSourceMediaStorageItemFetchFileFromUrl.post] File download from URL initiated.')
        return redirect('datasource_media_storages:list_items')
