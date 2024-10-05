#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: generate_description_media_item_views.py
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
#  File: generate_description_media_item_views.py
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

import re

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.llms.helpers.helper_prompts import GENERATE_FILE_DESCRIPTION_QUERY
from apps._services.tools.execution_handlers.storage_query_execution_handler import execute_storage_query
from apps._services.tools.utils import ExecutionTypesNames
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_media_storages.models import DataSourceMediaStorageItem
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceMediaStorageItemGenerateDescription(LoginRequiredMixin, TemplateView):
    """
    Generates a description for a specific media storage item based on its contents.

    This view uses a file type decoder to determine the appropriate execution type for generating the description. The generated description is then saved to the media storage item.

    Methods:
        get_context_data(self, **kwargs): Adds the generated description to the context for display.
        post(self, request, *args, **kwargs): Handles the description generation process for the media storage item.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        if 'generated_description' in kwargs:
            context['generated_description'] = kwargs['generated_description']
            print(f"Generated Description: {kwargs['generated_description']}")
        return context

    @staticmethod
    def decode_media_item_type(media_item_type):
        class MediaFileTypesNamesLists:
            IMAGE = ['jpg', 'png', 'gif', 'svg', 'bmp', 'tiff']
            AUDIO = ['mp3', 'wav', 'flac', 'aac', 'ogg']
            VIDEO = ['mp4', 'avi', 'mkv', 'mov']
            COMPRESSED = ['zip', 'rar', 'tar']
            CODE = ['py', 'js', 'ts', 'php', 'css', 'html', 'java', 'c', 'cpp', 'h', 'sh', 'go', 'dart']
            DATA = ['yml', 'yaml', 'sql', 'pkl', 'csv', 'xlsx', 'json', 'xml', 'tsv', 'docx', 'pptx', 'pdf', 'txt']

        if media_item_type in MediaFileTypesNamesLists.IMAGE:
            return ExecutionTypesNames.IMAGE_INTERPRETATION
        elif media_item_type in (MediaFileTypesNamesLists.COMPRESSED or
                                 media_item_type in MediaFileTypesNamesLists.DATA or
                                 media_item_type in MediaFileTypesNamesLists.CODE):
            return ExecutionTypesNames.FILE_INTERPRETATION
        else:
            # assume file interpretation
            return ExecutionTypesNames.FILE_INTERPRETATION

    @staticmethod
    def normalize_whitespace(text):
        # Remove leading and trailing whitespace
        text = text.strip()
        text = text.replace('\n', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\t', ' ')
        text = text.replace('\v', ' ')
        text = text.replace('\f', ' ')
        text = text.replace('\0', ' ')
        text = text.strip()
        # Replace all sequences of whitespace (including newlines, tabs, etc.) with a single space
        text = re.sub(r'\s+', ' ', text, flags=re.UNICODE)
        return text

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - UPDATE_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to update media files.")
            return redirect('datasource_media_storages:list_items')
        ##############################

        media_item_id = kwargs.get('pk')
        media_item = DataSourceMediaStorageItem.objects.get(id=media_item_id)
        execution_type = self.decode_media_item_type(media_item.media_file_type)
        texts, _, _ = execute_storage_query(chat_id=None,
                                            connection_id=media_item.storage_base.id,
                                            execution_type=execution_type,
                                            file_paths=[media_item.full_file_path],
                                            query=(GENERATE_FILE_DESCRIPTION_QUERY + f"""
                                                    File Type Information:
                                                    - Format: {media_item.media_file_type}
                                               """),
                                            without_chat=True)
        kwargs['pk'] = media_item_id
        if execution_type == ExecutionTypesNames.IMAGE_INTERPRETATION:
            generated_description = texts
            media_item.description = generated_description
            media_item.save()
        elif execution_type == ExecutionTypesNames.FILE_INTERPRETATION:
            try:
                response = texts["response"]
                generated_description = ""
                if response:
                    generated_description = response[0]
                # remove everything except a single space
                generated_description = self.normalize_whitespace(generated_description)
                media_item.description = generated_description
                media_item.save()
            except Exception as e:
                print(f"Error parsing generated description: {e}")
        return redirect('datasource_media_storages:item_detail', **kwargs)
