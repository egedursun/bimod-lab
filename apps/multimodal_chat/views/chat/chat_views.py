#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: chat_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import (
    redirect,
    get_object_or_404
)

from django.views.generic import TemplateView

from apps.beamguard.models import (
    BeamGuardArtifact
)

from apps.beamguard.utils import (
    BeamGuardConfirmationStatusesNames
)

from apps.core.media_managers.media_manager_execution_handler import (
    MediaManager
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.assistants.models import Assistant

from apps.message_templates.models import (
    MessageTemplate
)

from apps.multimodal_chat.models import (
    MultimodalChat,
    MultimodalChatMessage
)

from apps.multimodal_chat.utils import (
    SourcesForMultimodalChatsNames,
    generate_chat_name,
    ChatPostActionSpecifiers
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from config.settings import MEDIA_URL

from web_project import (
    TemplateLayout,
    TemplateHelper
)

logger = logging.getLogger(__name__)


class ChatView_Chat(LoginRequiredMixin, TemplateView):
    @staticmethod
    def refresh_page(chat_id, user_id):
        return (
            redirect
            (f'/chat/?chat_id={chat_id}')
        )

    def get_context_data(self, **kwargs):
        active_chat = None
        context_user = self.request.user

        if 'chat_id' in self.request.GET:
            active_chat = get_object_or_404(
                MultimodalChat,
                id=self.request.GET['chat_id'],
                user=self.request.user
            )

        chats = MultimodalChat.objects.filter(
            user=self.request.user,
            chat_source=SourcesForMultimodalChatsNames.APP,
            is_archived=False
        )

        artifacts = []
        if active_chat:
            chats = [active_chat] + [chat for chat in chats if chat.id != active_chat.id]

            artifacts = BeamGuardArtifact.objects.filter(
                assistant=active_chat.assistant,
                chat=active_chat,
                confirmation_status=BeamGuardConfirmationStatusesNames.PENDING,
            ).all()

        else:
            pass

        agents = Assistant.objects.filter(
            organization__users=self.request.user
        )

        orgs = Organization.objects.filter(
            assistants__in=agents
        )

        msg_tmpls = MessageTemplate.objects.filter(
            user=context_user,
            organization__in=orgs
        )

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        active_chat_msgs = active_chat.chat_messages.filter(
            hidden=False
        ).order_by('sent_at') if active_chat else None

        context.update(
            {
                "chats": chats,
                "assistants": agents,
                "active_chat": active_chat,
                "user": context_user,
                "chat_messages": active_chat_msgs,
                "message_templates": msg_tmpls,
                "base_url": MEDIA_URL,
                "artifacts": artifacts
            }
        )

        return context

    def post(self, request, *args, **kwargs):
        from apps.core.generative_ai.generative_ai_decode_manager import (
            GenerativeAIDecodeController
        )

        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_CHATS
        if not UserPermissionManager.is_authorized(
            user=context_user,
            operation=PermissionNames.CREATE_AND_USE_CHATS
        ):
            messages.error(self.request, "You do not have permission to create and use chats.")

            return redirect('multimodal_chat:chat')
        ##############################

        if ChatPostActionSpecifiers.NEW_CHAT_WITH_ASSISTANT_SPECIFIER in request.POST:

            agent_id = request.POST.get('assistant_id')

            agent = get_object_or_404(
                Assistant,
                id=agent_id,
                organization__users=request.user
            )

            chat = MultimodalChat.objects.create(
                organization=agent.organization,
                assistant=agent,
                user=request.user,
                chat_name=request.POST.get('chat_name', generate_chat_name()),
                created_by_user=request.user,
                chat_source=SourcesForMultimodalChatsNames.APP
            )

            active_chat = chat

        elif ChatPostActionSpecifiers.CHANGE_CHAT_NAME_SPECIFIER in request.POST:
            chat_id = request.POST.get('chat_id')

            chat = get_object_or_404(
                MultimodalChat,
                id=chat_id,
                user=request.user
            )

            chat.chat_name = request.POST.get('new_chat_name')

            chat.save()

            active_chat = chat

            logger.info(f"Chat name was changed by User: {context_user.id}.")

        elif ChatPostActionSpecifiers.STARRING_MESSAGE_SPECIFIER in request.POST:
            chat_id = request.POST.get('chat_id')

            chat = get_object_or_404(
                MultimodalChat,
                id=chat_id,
                user=request.user
            )

            msg_id = request.POST.get('message_id')

            msg = get_object_or_404(
                MultimodalChatMessage,
                id=msg_id,
                multimodal_chat=chat
            )

            msg.starred = not msg.starred

            msg.save()

            active_chat = chat

            logger.info(f"Message was starred by User: {context_user.id}.")

        else:
            (
                attached_fs,
                attached_imgs,
                chat,
                msg_content,
                sketch_image_full_uris_list
            ) = (
                self._handle_attached_images(request)
            )

            edit_image_full_uris_list = self._handle_edit_images(request)

            image_full_uris = self._handle_save_images(
                attached_imgs,
                edit_image_full_uris_list,
                sketch_image_full_uris_list
            )

            file_full_uris = self._handle_save_files(attached_fs)
            self._handle_record_audio(file_full_uris, request)

            user_message = MultimodalChatMessage.objects.create(
                multimodal_chat=chat,
                sender_type='USER',
                message_text_content=msg_content,
                message_image_contents=image_full_uris,
                message_file_contents=file_full_uris
            )

            internal_llm_client = GenerativeAIDecodeController.get(
                assistant=chat.assistant,
                multimodal_chat=chat
            )

            response = internal_llm_client.respond_stream(
                latest_message=user_message,
                image_uris=image_full_uris,
                file_uris=file_full_uris
            )

            MultimodalChatMessage.objects.create(
                multimodal_chat=chat,
                sender_type='ASSISTANT',
                message_text_content=response
            )

            active_chat = chat
            logger.info(f"Message was sent by User: {context_user.id}.")

        chats = MultimodalChat.objects.filter(
            user=request.user,
            chat_source=SourcesForMultimodalChatsNames.APP
        )

        agents = Assistant.objects.filter(
            organization__users=request.user
        )

        context.update(
            {
                "layout_path": TemplateHelper.set_layout(
                    "layout_vertical.html",
                    context
                ),
                'chat_id': active_chat.id if active_chat else None,
                'chats': chats,
                'assistants': agents,
                'active_chat': active_chat
            }
        )

        redirect_string = self.request.path_info + '?chat_id=' + str(active_chat.id)

        return redirect(
            redirect_string,
            *args,
            **kwargs
        )

    def _handle_attached_images(self, request):
        chat_id = request.POST.get('chat_id')

        chat = get_object_or_404(
            MultimodalChat,
            id=chat_id,
            user=request.user
        )

        msg_content = request.POST.get('message_content')
        attached_imgs = request.FILES.getlist('attached_images[]')
        attached_fs = request.FILES.getlist('attached_files[]')

        sketch_image = {
            'sketch_image': None
        }

        attached_canvas_image = request.POST.get('sketch_image')

        sketch_image_full_uris_list = []

        try:
            sketch_image_bytes = base64.b64decode(
                attached_canvas_image.split("base64,")[1].encode()
            )

            sketch_image['sketch_image'] = sketch_image_bytes

            sketch_image_full_uris_list = MediaManager.save_sketch(
                sketch_data_map=sketch_image
            )

            logger.info(f"Sketch image was saved by User: {request.user.id}.")

        except Exception as e:
            pass

        return attached_fs, attached_imgs, chat, msg_content, sketch_image_full_uris_list

    @staticmethod
    def _handle_edit_images(request):
        edit_image_bytes_dict = {
            'edit_image': None,
            'edit_image_mask': None
        }

        attached_edit_image = request.FILES.get('edit_image')
        attached_edit_image_mask = request.POST.get('edit_image_mask')

        edit_image_full_uris_list = []

        try:
            edit_image_bytes = attached_edit_image.read()

            edit_image_mask_bytes = base64.b64decode(
                attached_edit_image_mask.split("base64,")[1].encode()
            )

            edit_image_bytes_dict['edit_image'] = edit_image_bytes
            edit_image_bytes_dict['edit_image_mask'] = edit_image_mask_bytes

            edit_image_full_uris_list = MediaManager.save_edit_image_and_masked_image(
                edit_img_map=edit_image_bytes_dict
            )

            logger.info(f"Edit image was saved by User: {request.user.id}.")

        except Exception as e:
            pass

        return edit_image_full_uris_list

    @staticmethod
    def _handle_save_images(
        attached_imgs,
        edit_image_full_uris_list,
        sketch_image_full_uris_list
    ):
        image_bytes_list = []

        for image in attached_imgs:
            try:
                image_bytes = image.read()
                logger.info(f"Image was read.")

            except Exception as e:
                logger.error(f"Error reading image: {e}")
                continue

            image_bytes_list.append(
                image_bytes
            )

        image_full_uris = MediaManager.save_images_and_return_uris(
            image_bytes_list
        )

        if sketch_image_full_uris_list:
            image_full_uris.extend(
                sketch_image_full_uris_list
            )

        if edit_image_full_uris_list:
            image_full_uris.extend(
                edit_image_full_uris_list
            )

        return image_full_uris

    @staticmethod
    def _handle_save_files(attached_fs):
        file_bytes_list = []

        for file in attached_fs:
            file_name = file.name

            try:
                file_bytes = file.read()
                logger.info(f"File was read.")

            except Exception as e:
                logger.error(f"Error reading file: {e}")
                continue

            file_bytes_list.append(
                (
                    file_bytes,
                    file_name
                )
            )

        file_full_uris = MediaManager.save_files_and_return_uris(
            file_bytes_list
        )

        return file_full_uris

    @staticmethod
    def _handle_record_audio(
        file_full_uris,
        request
    ):

        record_audio = request.POST.get('record_audio')

        audio_full_uri = None

        if record_audio:
            audio_base_64 = request.POST.get('record_audio')

            audio_bytes = base64.b64decode(
                audio_base_64.split("base64,")[1].encode()
            )

            audio_full_uri = MediaManager.save_files_and_return_uris(
                [
                    (
                        audio_bytes,
                        'audio.webm'
                    )
                ]
            )[0]

        if audio_full_uri:
            file_full_uris.append(
                audio_full_uri
            )

        logger.info(f"Audio was saved by User: {request.user.id}.")

        return
