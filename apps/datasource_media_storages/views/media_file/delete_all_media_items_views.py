#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_all_media_items_views.py
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

import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_media_storages.models import DataSourceMediaStorageItem
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class MediaView_ItemDeleteAll(LoginRequiredMixin, TemplateView):
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

        mm_id = kwargs.get('id')
        complete_items_set = DataSourceMediaStorageItem.objects.filter(storage_base_id=mm_id)
        for item in complete_items_set:
            if item.full_file_path is not None:
                try:
                    os.system(f"rm -rf {item.full_file_path}")
                except Exception as e:
                    pass
        DataSourceMediaStorageItem.objects.filter(storage_base_id=mm_id).delete()
        messages.success(request, 'All media files deleted successfully.')
        return redirect('datasource_media_storages:list_items')
