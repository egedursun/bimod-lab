#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_media_item_views.py
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
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection, DataSourceMediaStorageItem
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class MediaView_ItemCreate(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user_agents = Assistant.objects.filter(organization__users__in=[request.user])
        media_managers = DataSourceMediaStorageConnection.objects.filter(assistant__in=user_agents)
        orgs = Organization.objects.filter(users__in=[request.user])

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = list(orgs.values('id', 'name'))
        context['assistants'] = list(user_agents.values('id', 'name', 'organization_id'))
        context['media_storages'] = list(media_managers.values('id', 'name', 'assistant_id'))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to add media files")
            return redirect('datasource_media_storages:list_items')
        ##############################

        mm_id = request.POST.get('media_storage') or None
        if not mm_id:
            messages.error(request, 'Please select a media storage.')
            return redirect('datasource_media_storages:create_item')
        media_manager = DataSourceMediaStorageConnection.objects.get(pk=mm_id)
        fs = request.FILES.getlist('media_files')
        descriptions = request.POST.getlist('file_descriptions[]')
        if mm_id and fs:
            for file, desc in zip(fs, descriptions):
                try:
                    f_data_bytes = file.read()
                except Exception as e:
                    messages.error(request, f'Error reading file: {e}')
                    continue
                media_item = DataSourceMediaStorageItem.objects.create(
                    storage_base=media_manager, media_file_name=file.name.split('.')[0],
                    media_file_size=file.size, media_file_type=file.name.split('.')[-1],
                    file_bytes=f_data_bytes, description=desc
                )
                media_item.save()
            logger.info(f"[views.create_media_item] Files uploaded successfully.")
            messages.success(request, 'Files uploaded successfully.')
            return redirect('datasource_media_storages:list_items')
        else:
            logger.error('Please select a media storage and upload files.')
            messages.error(request, 'Please select a media storage and upload files.')
        return redirect('datasource_media_storages:create_item')
