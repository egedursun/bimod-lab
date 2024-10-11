#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: fetch_media_file_from_url_views.py
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
from apps.datasource_media_storages.tasks import download_file_from_url
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class MediaView_ItemHTTPRetrieval(LoginRequiredMixin, TemplateView):
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

        mm_id = request.POST.get('storage_id') or None
        if not mm_id:
            messages.error(request, 'Invalid media storage ID.')
            return redirect('datasource_media_storages:create_item')
        retrieval_uri = request.POST.get('download_url') or None
        if not retrieval_uri:
            messages.error(request, 'Invalid download URL.')
            return redirect('datasource_media_storages:create_item')
        mm_id_int = int(mm_id)
        download_file_from_url.delay(storage_id=mm_id_int, url=retrieval_uri)
        messages.success(request, 'File download from URL initiated.')
        return redirect('datasource_media_storages:list_items')
