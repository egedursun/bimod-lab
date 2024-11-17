#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: generated_media_items_views.py
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
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_media_storages.models import DataSourceMediaStorageItem
from apps.multimodal_chat.models import MultimodalChat
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from apps.video_generations.models import GeneratedVideo
from config.settings import MEDIA_URL
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class MediaView_Generated(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_STORAGE_FILES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_STORAGE_FILES):
            messages.error(self.request, "You do not have permission to see media files.")
            return context
        ##############################

        try:
            orgs = Organization.objects.filter(users__in=[self.request.user])
            data = []
            for org in orgs:
                agents = Assistant.objects.filter(organization=org)
                agent_data_list = []
                for agent in agents:
                    chats_of_agents = MultimodalChat.objects.filter(assistant=agent)
                    msgs_with_imgs = []
                    msgs_with_fs = []
                    for chat in chats_of_agents:
                        f_or_img_msgs = chat.chat_messages.filter(Q(message_image_contents__isnull=False) |
                                                                  Q(message_file_contents__isnull=False))
                        for m in f_or_img_msgs:
                            if m.message_image_contents:
                                for img in m.message_image_contents:
                                    message_data = {'message': m, 'image': img}
                                    msgs_with_imgs.append(message_data)
                            if m.message_file_contents:
                                for file in m.message_file_contents:
                                    message_data = {'message': m, 'file': file}
                                    msgs_with_fs.append(message_data)

                    pg_imgs = Paginator(msgs_with_imgs, 5)  # 5 items per page
                    pg_no_imgs = self.request.GET.get('page_images')
                    pg_obj_imgs = pg_imgs.get_page(pg_no_imgs)
                    pg_fs = Paginator(msgs_with_fs, 5)
                    pg_no_fs = self.request.GET.get('page_files')
                    pg_obj_fs = pg_fs.get_page(pg_no_fs)
                    gen_videos = GeneratedVideo.objects.filter(assistant=agent)
                    pg_videos = Paginator(gen_videos, 5)
                    pg_no_videos = self.request.GET.get('page_videos')
                    pg_obj_videos = pg_videos.get_page(pg_no_videos)

                    agent_data = {
                        'assistant': agent, 'messages_with_images': pg_obj_imgs, 'messages_with_files': pg_obj_fs,
                        'generated_videos': pg_obj_videos,
                    }
                    agent_data_list.append(agent_data)
                data.append({'organization': org, 'assistants': agent_data_list, })
        except Exception as e:
            logger.error(f"User: {self.request.user} - Generated Media - List Error: {e}")
            messages.error(self.request, 'An error occurred while listing generated media files.')
            return context

        context['data'] = data
        context['base_url'] = MEDIA_URL
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
                        s3c = boto3.client('s3')
                        bucket = os.getenv('AWS_STORAGE_BUCKET_NAME')
                        s3c.delete_object(Bucket=bucket, Key=item.full_file_path.split(MEDIA_URL)[1])
                    except Exception as e:
                        pass
            logger.info(f"[views.generated_media_items] Deleting selected generated media files.")
            DataSourceMediaStorageItem.objects.filter(id__in=item_ids).delete()

        messages.success(request, 'Selected generated media files deleted successfully.')
        return redirect('datasource_media_storages:list_items')
