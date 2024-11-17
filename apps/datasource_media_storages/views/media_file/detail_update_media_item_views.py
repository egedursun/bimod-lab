#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: detail_update_media_item_views.py
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
import os

import boto3
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_media_storages.models import DataSourceMediaStorageItem
from apps.datasource_media_storages.utils import decode_stream__docx, decode_stream__pptx, decode_stream__xlsx, \
    FILE_TYPE_HIGHLIGHTING_DECODER, MediaManagerItemFormatTypesNames
from apps.user_permissions.utils import PermissionNames
from config.settings import MEDIA_URL
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class MediaView_ItemUpdate(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to see media files.")
            return context
        ##############################

        media_item = DataSourceMediaStorageItem.objects.get(id=kwargs['pk'])
        context['media_item'] = media_item
        f_data_bytes = None
        if media_item.full_file_path is not None:
            try:
                s3c = boto3.client('s3')
                bucket = os.getenv('AWS_STORAGE_BUCKET_NAME')
                f_data_bytes = s3c.get_object(Bucket=bucket, Key=media_item.full_file_path.split(MEDIA_URL)[1])
                f_data_bytes = f_data_bytes['Body'].read()
            except Exception as e:
                pass

        item_contents = "File contents could not be decoded."
        try:
            if media_item.media_file_type == MediaManagerItemFormatTypesNames.Data.TXT:
                item_contents = f_data_bytes.decode('utf-8')
            elif media_item.media_file_type == MediaManagerItemFormatTypesNames.Data.DOCX:
                item_contents = decode_stream__docx(f_data_bytes)
            elif media_item.media_file_type == MediaManagerItemFormatTypesNames.Data.PPTX:
                item_contents = decode_stream__pptx(f_data_bytes)
            elif media_item.media_file_type == MediaManagerItemFormatTypesNames.Data.XLSX:
                item_contents = decode_stream__xlsx(f_data_bytes)
            else:
                item_contents = f_data_bytes.decode('utf-8', errors='ignore')
        except Exception as e:
            pass
        context['media_item_contents'] = item_contents
        context['file_type_highlighting'] = FILE_TYPE_HIGHLIGHTING_DECODER.get(media_item.media_file_type, 'plaintext')
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - UPDATE_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to update media files.")
            return redirect('datasource_media_storages:list_items')
        ##############################

        try:
            media_item = DataSourceMediaStorageItem.objects.get(id=kwargs['pk'])
            description = request.POST.get('description')
            media_item.description = description
            media_item.save()
        except Exception as e:
            logger.error(f"User: {request.user} - Media Item - Update Error: {e}")
            messages.error(request, 'An error occurred while updating the media item.')
            return redirect('datasource_media_storages:list_items')

        logger.info(f"[views.update_media_item] Media item updated successfully.")
        messages.success(request, 'Media item updated successfully.')
        return redirect('datasource_media_storages:list_items')
