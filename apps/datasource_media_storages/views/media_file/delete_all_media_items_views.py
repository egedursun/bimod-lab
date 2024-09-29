#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: delete_all_media_items_views.py
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

import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_media_storages.models import DataSourceMediaStorageItem
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceMediaStorageAllItemsDeleteView(LoginRequiredMixin, TemplateView):
    """
    Handles deleting all media items within a specific media storage connection.

    This view allows users with the appropriate permissions to delete all media items in a selected media storage connection. It ensures that the user has the necessary permissions before performing the deletion.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for rendering the confirmation of the deletion.
        post(self, request, *args, **kwargs): Deletes all media items in the selected media storage connection if the user has the required permissions.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.post(request, *args, **kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to delete media files.")
            return redirect('datasource_media_storages:list_items')
        ##############################

        base_id = kwargs.get('id')
        all_items = DataSourceMediaStorageItem.objects.filter(storage_base_id=base_id)
        for item in all_items:
            if item.full_file_path is not None:
                try:
                    os.system(f"rm -rf {item.full_file_path}")
                except Exception as e:
                    print(f"Error deleting the file from the media storage path: {item.full_file_path} // {e}")
        DataSourceMediaStorageItem.objects.filter(storage_base_id=base_id).delete()
        messages.success(request, 'All media files deleted successfully.')
        print('[DataSourceMediaStorageAllItemsDeleteView.post] All media files deleted successfully.')
        return redirect('datasource_media_storages:list_items')
