#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_orchestration_queries_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


import base64
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.orchestration.orchestration_executor import OrchestrationExecutor
from apps.core.media_managers.media_manager_execution_handler import MediaManager
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.orchestrations.models import Maestro, OrchestrationQuery, OrchestrationQueryLog
from apps.orchestrations.utils import OrchestrationQueryLogTypesNames
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class OrchestrationView_QueryList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        maestro_id = kwargs['pk']
        maestro = get_object_or_404(Maestro, id=maestro_id)
        query_chats = OrchestrationQuery.objects.filter(created_by_user=self.request.user, maestro=maestro)
        context['maestro'] = maestro
        context['query_chats'] = query_chats
        context['maestro_list'] = Maestro.objects.all()
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_ORCHESTRATION_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_AND_USE_ORCHESTRATION_CHATS):
            messages.error(self.request, "You do not have permission to create and use orchestration queries.")
            return redirect('orchestrations:list')
        ##############################

        maestro_id = request.POST.get('maestro_id')
        query_text = request.POST.get('query_text')
        attached_images = request.FILES.getlist('attached_images[]')
        attached_files = request.FILES.getlist('attached_files[]')

        sketch_image_full_uris_list = self._handle_sketch_image(request)
        edit_image_full_uris_list = self._handle_edit_image(request)
        self._handle_save_images(attached_images, edit_image_full_uris_list, sketch_image_full_uris_list)
        file_full_uris = self._handle_save_files(attached_files)
        self._handle_record_audio(file_full_uris, request)
        maestro = get_object_or_404(Maestro, id=maestro_id)
        query_chat = OrchestrationQuery.objects.create(
            maestro=maestro, query_text=query_text, created_by_user=request.user, last_updated_by_user=request.user)
        query_log = OrchestrationQueryLog.objects.create(
            orchestration_query=query_chat, log_type=OrchestrationQueryLogTypesNames.USER,
            log_text_content=query_text, log_file_contents=None, log_image_contents=None)
        query_chat.logs.add(query_log)
        query_chat.save()
        orch_xc = OrchestrationExecutor(maestro=maestro, query_chat=query_chat)
        final_response = orch_xc.execute_for_query()

        logger.info(f"Orchestration query was created by User: {self.request.user.id}.")
        return redirect('orchestrations:query_detail', pk=maestro_id, query_id=query_chat.id)

    @staticmethod
    def _handle_record_audio(file_full_uris, request):
        record_audio = request.POST.get('record_audio')
        audio_full_uri = None
        if record_audio:
            audio_base_64 = request.POST.get('record_audio')
            audio_bytes = base64.b64decode(audio_base_64.split("base64,")[1].encode())
            audio_full_uri = MediaManager.save_files_and_return_uris([(audio_bytes, 'audio.webm')])[0]
        if audio_full_uri:
            file_full_uris.append(audio_full_uri)
        logger.info(f"Audio was saved successfully.")
        return

    @staticmethod
    def _handle_save_files(attached_files):
        file_bytes_list = []
        for file in attached_files:
            file_name = file.name
            try:
                file_bytes = file.read()
                logger.info(f"File was saved successfully.")
            except Exception as e:
                logger.error(f"File was not saved successfully.")
                continue
            file_bytes_list.append((file_bytes, file_name))
        file_full_uris = MediaManager.save_files_and_return_uris(file_bytes_list)
        return file_full_uris

    @staticmethod
    def _handle_save_images(attached_images, edit_image_full_uris_list, sketch_image_full_uris_list):
        image_bytes_list = []
        for image in attached_images:
            try:
                image_bytes = image.read()
                logger.info(f"Image was saved successfully.")
            except Exception as e:
                logger.error(f"Image was not saved successfully.")
                continue
            image_bytes_list.append(image_bytes)
        image_full_uris = MediaManager.save_images_and_return_uris(image_bytes_list)
        if sketch_image_full_uris_list:
            image_full_uris.extend(sketch_image_full_uris_list)
        if edit_image_full_uris_list:
            image_full_uris.extend(edit_image_full_uris_list)

    @staticmethod
    def _handle_edit_image(request):
        edit_image_bytes_dict = {'edit_image': None, 'edit_image_mask': None}
        attached_edit_image = request.FILES.get('edit_image')
        attached_edit_image_mask = request.POST.get('edit_image_mask')
        edit_image_full_uris_list = []
        try:
            edit_image_bytes = attached_edit_image.read()
            edit_image_mask_bytes = base64.b64decode(attached_edit_image_mask.split("base64,")[1].encode())
            edit_image_bytes_dict['edit_image'] = edit_image_bytes
            edit_image_bytes_dict['edit_image_mask'] = edit_image_mask_bytes
            edit_image_full_uris_list = MediaManager.save_edit_image_and_masked_image(
                edit_img_map=edit_image_bytes_dict)
            logger.info(f"Edit image was saved successfully.")
        except Exception as e:
            logger.error(f"Edit image was not saved successfully.")
            pass
        return edit_image_full_uris_list

    @staticmethod
    def _handle_sketch_image(request):
        sketch_image = {'sketch_image': None}
        attached_canvas_image = request.POST.get('sketch_image')
        sketch_image_full_uris_list = []
        try:
            sketch_image_bytes = base64.b64decode(attached_canvas_image.split("base64,")[1].encode())
            sketch_image['sketch_image'] = sketch_image_bytes
            sketch_image_full_uris_list = MediaManager.save_sketch(sketch_data_map=sketch_image)
            logger.info(f"Sketch image was saved successfully.")
        except Exception as e:
            logger.error(f"Sketch image was not saved successfully.")
            pass
        return sketch_image_full_uris_list
