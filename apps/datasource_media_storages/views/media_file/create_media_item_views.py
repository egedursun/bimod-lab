#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: create_media_item_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: create_media_item_views.py
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
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection, DataSourceMediaStorageItem
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceMediaStorageItemCreateView(LoginRequiredMixin, TemplateView):
    """
    Handles uploading media files to a selected media storage connection.

    This view displays a form for selecting a media storage connection and uploading media files to it. Upon form submission, it validates the input, reads the file contents, and saves the media items to the database. If the user lacks the necessary permissions, an error message is displayed.

    Methods:
        get(self, request, *args, **kwargs): Prepares the context with the available media storage connections and assistants for media file uploading.
        post(self, request, *args, **kwargs): Handles the media file upload process, including validation and saving the media items.
    """

    def get(self, request, *args, **kwargs):
        user_assistants = Assistant.objects.filter(organization__users__in=[request.user])
        media_storages = DataSourceMediaStorageConnection.objects.filter(assistant__in=user_assistants)
        organizations = Organization.objects.filter(users__in=[request.user])

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = list(organizations.values('id', 'name'))
        context['assistants'] = list(user_assistants.values('id', 'name', 'organization_id'))
        context['media_storages'] = list(media_storages.values('id', 'name', 'assistant_id'))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to add media files")
            return redirect('datasource_media_storages:list_items')
        ##############################

        media_storage_id = request.POST.get('media_storage') or None
        # PERMISSION CHECK FOR - MEDIA ITEM / CREATE
        context_user = self.request.user
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type', flat=True))
        if PermissionNames.ADD_MEDIA_STORAGES not in user_permissions:
            messages.error(request, "You do not have permission to create media items.")
            return redirect('datasource_media_storages:list_items')

        if not media_storage_id:
            messages.error(request, 'Please select a media storage.')
            return redirect('datasource_media_storages:create_item')
        media_storage = DataSourceMediaStorageConnection.objects.get(pk=media_storage_id)
        files = request.FILES.getlist('media_files')
        descriptions = request.POST.getlist('file_descriptions[]')
        if media_storage_id and files:
            for file, description in zip(files, descriptions):
                try:
                    file_bytes = file.read()
                except Exception as e:
                    messages.error(request, f'Error reading file: {e}')
                    continue
                media_storage_item = DataSourceMediaStorageItem.objects.create(
                    storage_base=media_storage,
                    media_file_name=file.name.split('.')[0],
                    media_file_size=file.size,
                    media_file_type=file.name.split('.')[-1],
                    file_bytes=file_bytes,
                    description=description
                )
                media_storage_item.save()
            print('[DataSourceMediaStorageItemCreateView.post] Files uploaded successfully.')
            messages.success(request, 'Files uploaded successfully.')
            return redirect('datasource_media_storages:list_items')
        else:
            messages.error(request, 'Please select a media storage and upload files.')
        return redirect('datasource_media_storages:create_item')
