#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: main_workspace_views.py
#  Last Modified: 2024-11-12 23:00:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-12 23:00:13
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

from apps.assistants.models import Assistant
from apps.beamguard.models import BeamGuardArtifact

from apps.beamguard.utils import (
    BeamGuardConfirmationStatusesNames
)

from apps.core.media_managers.media_manager_execution_handler import (
    MediaManager
)

from apps.core.tool_calls.utils import (
    VoidForgerModesNames
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)
from apps.llm_core.models import LLMCore

from apps.message_templates.models import MessageTemplate
from apps.multimodal_chat.models import MultimodalChat

from apps.multimodal_chat.utils import (
    SourcesForMultimodalChatsNames,
    ChatPostActionSpecifiers,
    generate_chat_name
)

from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames

from apps.voidforger.models import (
    MultimodalVoidForgerChat,
    MultimodalVoidForgerChatMessage,
    VoidForger
)

from config.settings import MEDIA_URL
from web_project import TemplateLayout, TemplateHelper

logger = logging.getLogger(__name__)


class ChatView_MainWorkspace(TemplateView, LoginRequiredMixin):

    @staticmethod
    def refresh_page(chat_id, user_id):
        return redirect(f'/workspace/?chat_id={chat_id}')

    def get_context_data(self, **kwargs):

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context.update(
            {
                "layout": "blank",
                "layout_path": TemplateHelper.set_layout(
                    "layout_blank.html",
                    context
                ),
            }
        )

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        llm_models = LLMCore.objects.filter(
            organization__in=user_orgs
        )

        if not llm_models or len(llm_models) == 0:
            messages.error(self.request, "You do not have an LLM model to use, to use VoidForger chat, please create an LLM model.")
            return context

        voidforger_object, _ = VoidForger.objects.get_or_create(
            user=self.request.user
        )

        if voidforger_object.llm_model is None:
            voidforger_object.llm_model = llm_models[0]
            voidforger_object.save()

        active_chat = None
        context_user = self.request.user

        if 'chat_id' in self.request.GET:
            active_chat = get_object_or_404(
                MultimodalVoidForgerChat,
                id=self.request.GET['chat_id'],
                user=self.request.user
            )

        chats = MultimodalVoidForgerChat.objects.filter(
            user=self.request.user,
            chat_source=SourcesForMultimodalChatsNames.APP
        )

        artifacts = []
        if active_chat:
            chats = [active_chat] + [chat for chat in chats if chat.id != active_chat.id]

            voidforger_orgs = active_chat.voidforger.organizations.all()

            all_assistants_of_orgs = Assistant.objects.filter(
                organization__in=voidforger_orgs
            )

            standard_assistant_chats = MultimodalChat.objects.filter(
                assistant__in=all_assistants_of_orgs
            )

            artifacts = BeamGuardArtifact.objects.filter(
                assistant__in=all_assistants_of_orgs,
                chat__in=standard_assistant_chats,
                confirmation_status=BeamGuardConfirmationStatusesNames.PENDING,
            ).all()

            artifacts = list(set(artifacts))

        else:
            pass

        orgs = Organization.objects.filter(
            users__in=[context_user]
        )

        msg_templates = MessageTemplate.objects.filter(
            user=context_user,
            organization__in=orgs
        )

        active_chat_msgs = active_chat.voidforger_chat_messages.filter(
            hidden=False
        ).order_by('sent_at') if active_chat else None

        context.update(
            {
                "layout": "blank",
                "layout_path": TemplateHelper.set_layout(
                    "layout_blank.html",
                    context
                ),
                "chats": chats,
                "active_chat": active_chat,
                "user": context_user,
                "chat_messages": active_chat_msgs,
                "message_templates": msg_templates,
                "base_url": MEDIA_URL,
                "artifacts": artifacts,
            }
        )

        return context

    def post(
        self,
        request,
        *args,
        **kwargs
    ):

        from apps.core.generative_ai.generative_ai_decode_manager import GenerativeAIDecodeController
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_VOIDFORGER_CHATS
        if not UserPermissionManager.is_authorized(
            user=context_user,
            operation=PermissionNames.CREATE_AND_USE_VOIDFORGER_CHATS
        ):
            messages.error(self.request, "You do not have permission to create and use VoidForger chats.")
            return redirect('multimodal_chat:main_workspace')
        ##############################

        if ChatPostActionSpecifiers.NEW_CHAT_WITH_ASSISTANT_SPECIFIER in request.POST:

            voidforger = get_object_or_404(
                VoidForger,
                user=request.user
            )

            chat = MultimodalVoidForgerChat.objects.create(
                voidforger=voidforger,
                user=request.user,
                chat_name=request.POST.get('chat_name', generate_chat_name()),
                created_by_user=request.user,
                chat_source=SourcesForMultimodalChatsNames.APP
            )
            active_chat = chat

        elif ChatPostActionSpecifiers.CHANGE_CHAT_NAME_SPECIFIER in request.POST:

            chat_id = request.POST.get('chat_id')

            chat = get_object_or_404(
                MultimodalVoidForgerChat,
                id=chat_id,
                user=request.user
            )

            chat.chat_name = request.POST.get('new_chat_name')
            chat.save()
            active_chat = chat

        else:
            chat_id = request.POST.get('chat_id')

            chat = get_object_or_404(
                MultimodalVoidForgerChat,
                id=chat_id,
                user=request.user
            )

            msg_content = request.POST.get('message_content')
            attached_images = request.FILES.getlist('attached_images[]')
            attached_files = request.FILES.getlist('attached_files[]')

            sketch_image_full_uris_list = self._handle_sketch_image(request)
            edit_image_full_uris_list = self._handle_edit_image(request)

            image_full_uris = self._handle_save_images(
                attached_images,
                edit_image_full_uris_list,
                sketch_image_full_uris_list
            )

            file_full_uris = self._handle_save_files(attached_files)
            self._handle_record_audio(file_full_uris, request)

            user_msg = MultimodalVoidForgerChatMessage.objects.create(
                multimodal_voidforger_chat=chat,
                sender_type='USER',
                message_text_content=msg_content,
                message_image_contents=image_full_uris,
                message_file_contents=file_full_uris
            )

            internal_llm_client_voidforger = GenerativeAIDecodeController.get_voidforger(
                user=request.user,
                assistant=chat.voidforger,
                multimodal_chat=chat
            )

            response = internal_llm_client_voidforger.respond(
                latest_message=user_msg,
                current_mode=VoidForgerModesNames.CHAT,
                image_uris=image_full_uris,
                file_uris=file_full_uris
            )

            MultimodalVoidForgerChatMessage.objects.create(
                multimodal_voidforger_chat=chat,
                sender_type='ASSISTANT',
                message_text_content=response

            )
            active_chat = chat

        chats = MultimodalVoidForgerChat.objects.filter(
            user=request.user,
            chat_source=SourcesForMultimodalChatsNames.APP
        )

        context.update(
            {
                "layout_path": TemplateHelper.set_layout(
                    "layout_vertical.html",
                    context
                ),
                'chat_id': active_chat.id if active_chat else None,
                'chats': chats,
                'active_chat': active_chat
            }
        )

        redirect_string = self.request.path_info + '?chat_id=' + str(active_chat.id)

        logger.info(f"VoidForger chat was streamed by User: {context_user.id}.")
        return redirect(redirect_string, *args, **kwargs)

    @staticmethod
    def _handle_record_audio(
        file_full_uris,
        request
    ):
        record_audio = request.POST.get('record_audio')
        audio_full_uri = None

        if record_audio:
            audio_base_64 = request.POST.get('record_audio')
            audio_bytes = base64.b64decode(audio_base_64.split("base64,")[1].encode())
            audio_full_uri = MediaManager.save_files_and_return_uris([(audio_bytes, 'audio.webm')])[0]

        if audio_full_uri:
            file_full_uris.append(
                audio_full_uri
            )

        logger.info(f"Audio was recorded successfully.")
        return

    @staticmethod
    def _handle_save_files(attached_files):
        file_bytes_list = []

        for file in attached_files:
            file_name = file.name

            try:
                file_bytes = file.read()
                logger.info(f"File: {file_name} was read successfully.")

            except Exception as e:
                logger.error(f"Error while reading file: {file_name}.")
                continue

            file_bytes_list.append((file_bytes, file_name))

        file_full_uris = MediaManager.save_files_and_return_uris(file_bytes_list)
        return file_full_uris

    @staticmethod
    def _handle_save_images(
        attached_images,
        edit_image_full_uris_list,
        sketch_image_full_uris_list
    ):

        image_bytes_list = []

        for image in attached_images:

            try:
                image_bytes = image.read()
                logger.info(f"Image: {image.name} was read successfully.")

            except Exception as e:
                logger.error(f"Error while reading image: {image.name}.")
                continue

            image_bytes_list.append(image_bytes)

        image_full_uris = MediaManager.save_images_and_return_uris(image_bytes_list)

        if sketch_image_full_uris_list:
            image_full_uris.extend(sketch_image_full_uris_list)

        if edit_image_full_uris_list:
            image_full_uris.extend(edit_image_full_uris_list)

        return image_full_uris

    @staticmethod
    def _handle_edit_image(request):

        edit_image_bytes_dict = {
            'edit_image': None,
            'edit_image_mask': None
        }

        attached_edit_image = request.FILES.get('edit_image')
        attached_edit_image_mask = request.POST.get('edit_image_mask')
        edit_image_full_uris_list = []

        try:
            edit_image_bytes = attached_edit_image.read()
            edit_image_mask_bytes = base64.b64decode(attached_edit_image_mask.split("base64,")[1].encode())
            edit_image_bytes_dict['edit_image'] = edit_image_bytes
            edit_image_bytes_dict['edit_image_mask'] = edit_image_mask_bytes

            edit_image_full_uris_list = MediaManager.save_edit_image_and_masked_image(
                edit_img_map=edit_image_bytes_dict
            )

            logger.info(f"Edit image was saved successfully.")

        except Exception as e:
            logger.error(f"Error while saving edit image.")
            pass

        return edit_image_full_uris_list

    @staticmethod
    def _handle_sketch_image(request):
        sketch_image = {
            'sketch_image': None
        }

        attached_canvas_image = request.POST.get('sketch_image')
        sketch_image_full_uris_list = []

        try:
            sketch_image_bytes = base64.b64decode(attached_canvas_image.split("base64,")[1].encode())
            sketch_image['sketch_image'] = sketch_image_bytes

            sketch_image_full_uris_list = MediaManager.save_sketch(
                sketch_data_map=sketch_image
            )

            logger.info(f"Sketch image was saved successfully.")

        except Exception as e:
            logger.error(f"Error while saving sketch image.")
            pass

        return sketch_image_full_uris_list
