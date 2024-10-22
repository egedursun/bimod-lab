#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: generate_description_media_item_views.py
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
import re

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.generative_ai.auxiliary_methods.tool_helpers.tool_helper_instructions import \
    FILE_GENERATION_INSTRUCTION_QUERY
from apps.core.tool_calls.core_services.core_service_query_media_manager import run_query_media_manager
from apps.core.tool_calls.utils import AnalysisToolCallExecutionTypesNames
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_media_storages.models import DataSourceMediaStorageItem
from apps.datasource_media_storages.utils import MediaManagerItemFormatTypesNamesLists, \
    AI_GENERATED_DESCRIPTION_SPECIFIER
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class MediaView_ItemAIDescription(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        if AI_GENERATED_DESCRIPTION_SPECIFIER in kwargs:
            context['generated_description'] = kwargs['generated_description']
        return context

    @staticmethod
    def decode_media_item_type(media_item_type):
        class MediaFileTypesNamesLists:
            IMAGE = MediaManagerItemFormatTypesNamesLists.IMAGE
            AUDIO = MediaManagerItemFormatTypesNamesLists.AUDIO
            VIDEO = MediaManagerItemFormatTypesNamesLists.VIDEO
            COMPRESSED = MediaManagerItemFormatTypesNamesLists.COMPRESSED
            CODE = MediaManagerItemFormatTypesNamesLists.CODE
            DATA = MediaManagerItemFormatTypesNamesLists.DATA

        if media_item_type in MediaFileTypesNamesLists.IMAGE:
            logger.info(f"Media Item Type: {media_item_type}")
            return AnalysisToolCallExecutionTypesNames.IMAGE_INTERPRETATION
        elif media_item_type in (
            MediaFileTypesNamesLists.COMPRESSED or
            media_item_type in MediaFileTypesNamesLists.DATA or
            media_item_type in MediaFileTypesNamesLists.CODE):
            logger.info(f"Media Item Type: {media_item_type}")
            return AnalysisToolCallExecutionTypesNames.FILE_INTERPRETATION
        else:
            logger.info(f"Media Item Type: {media_item_type}")
            return AnalysisToolCallExecutionTypesNames.FILE_INTERPRETATION

    @staticmethod
    def normalize_whitespace(text):
        text = text.strip()
        text = text.replace('\n', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\t', ' ')
        text = text.replace('\v', ' ')
        text = text.replace('\f', ' ')
        text = text.replace('\0', ' ')
        text = text.strip()
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

        item_id = kwargs.get('pk')
        media_item = DataSourceMediaStorageItem.objects.get(id=item_id)
        xc_type = self.decode_media_item_type(media_item.media_file_type)
        txts, _, _ = run_query_media_manager(chat_id=None, c_id=media_item.storage_base.id,
                                             manager_file_type=xc_type, f_uris=[media_item.full_file_path],
                                             manager_query=(FILE_GENERATION_INSTRUCTION_QUERY + f"""
                                                    File Format Information:
                                                    - Extension/Type: {media_item.media_file_type}
                                               """),
                                             no_chat=True)
        kwargs['pk'] = item_id
        if xc_type == AnalysisToolCallExecutionTypesNames.IMAGE_INTERPRETATION:
            gen_desc = txts
            media_item.description = gen_desc
            media_item.save()
        elif xc_type == AnalysisToolCallExecutionTypesNames.FILE_INTERPRETATION:
            try:
                output = txts["response"]
                gen_desc = ""
                if output:
                    gen_desc = output[0]
                gen_desc = self.normalize_whitespace(gen_desc)
                media_item.description = gen_desc
                media_item.save()
                logger.info(f"[views.update_media_item] Media item updated successfully.")
            except Exception as e:
                logger.error(f"Error while updating media item description: {e}")
                pass
        return redirect('datasource_media_storages:item_detail', **kwargs)
