#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: chat_history_factory_builder.py
#  Last Modified: 2024-10-05 02:26:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
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
import uuid

import requests

from apps.core.context_memory_manager.context_memory_manager import (
    ContextMemoryManager
)

from apps.core.data_security.ner.ner_executor import (
    NERExecutor
)

from apps.llm_transaction.models import LLMTransaction

from apps.multimodal_chat.models import (
    MultimodalChat,
    MultimodalLeanChat
)

import base64 as b64

from apps.voidforger.models import (
    MultimodalVoidForgerChat
)

logger = logging.getLogger(__name__)


class HistoryBuilder:
    class ChatRoles:
        SYSTEM = "SYSTEM"
        USER = "USER"
        ASSISTANT = "ASSISTANT"
        TOOL = "TOOL"

    @staticmethod
    def build_chat_history(
        chat: MultimodalChat,
        ner_executor: NERExecutor = None
    ):

        from apps.core.generative_ai.utils import (
            GPT_DEFAULT_ENCODING_ENGINE
        )

        msgs = chat.chat_messages.all().order_by("sent_at")

        history = []

        temporary_uuid = uuid.uuid4()

        for msg in msgs:

            src_type = msg.sender_type

            if src_type == HistoryBuilder.ChatRoles.TOOL:
                src_type = HistoryBuilder.ChatRoles.ASSISTANT

            message_text_content = msg.message_text_content

            msg_img_urls = msg.message_image_contents
            msg_f_urls = msg.message_file_contents

            msg_obj = {
                "role": src_type.lower()
            }

            wrapper = [
                {
                    "type": "text",
                    "text": message_text_content
                }
            ]

            if msg_img_urls and src_type == HistoryBuilder.ChatRoles.USER:

                for img_url in msg_img_urls:

                    uri = f"{img_url}"

                    try:
                        output = requests.get(uri)
                        data_bytes = output.content
                        image_b64 = b64.b64encode(data_bytes).decode("utf-8")

                    except Exception as e:
                        logger.error(f"Error while fetching image content: {e}")
                        continue

                    img_wrapper = {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{img_url.split('.')[-1]};base64,{image_b64}"
                        }
                    }

                    img_uri_wrapper = {
                        "type": "text",
                        "text": f"Detected Image URLs: {img_url}"
                    }

                    wrapper.append(img_wrapper)
                    wrapper.append(img_uri_wrapper)

            if msg_f_urls and src_type == HistoryBuilder.ChatRoles.USER:

                for f_url in msg_f_urls:
                    file_uri_info_wrapper = {
                        "type": "text",
                        "text": f"Detected File URLs: {f_url}"
                    }

                    wrapper.append(file_uri_info_wrapper)

            msg_obj["content"] = wrapper

            if src_type != HistoryBuilder.ChatRoles.SYSTEM:

                ####################################################################################################
                # NER INTEGRATION - ENCRYPTION
                ####################################################################################################

                if ner_executor:

                    encrypted_text = ner_executor.encrypt_text(
                        text=message_text_content,
                        uuid_str=temporary_uuid
                    )

                    if encrypted_text:
                        wrapper = [
                            {
                                "type": "text",
                                "text": encrypted_text
                            }
                        ]
                        msg_obj["content"] = wrapper

                ####################################################################################################
                ####################################################################################################

                history.append(msg_obj)

            tx = LLMTransaction.objects.create(
                organization=chat.organization,
                model=chat.assistant.llm_model,
                responsible_user=chat.user,
                responsible_assistant=chat.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=message_text_content,
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=src_type.lower(),
                transaction_source=chat.chat_source
            )

            logger.info(f"Chat Transaction: {tx}")
            chat.transactions.add(tx)

            chat.save()
            msg.save()

        history = ContextMemoryManager.handle_context(
            chat_history=history,
            assistant=chat.assistant
        )

        return history, temporary_uuid

    @staticmethod
    def build_leanmod(lean_chat: MultimodalLeanChat):

        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        msgs = lean_chat.lean_chat_messages.all().order_by("sent_at")

        history = []
        temporary_uuid = uuid.uuid4()

        for msg in msgs:

            source_type = msg.sender_type
            if source_type == HistoryBuilder.ChatRoles.TOOL:
                source_type = HistoryBuilder.ChatRoles.ASSISTANT

            txt_content = msg.message_text_content

            img_urls = msg.message_image_contents
            f_urls = msg.message_file_contents

            msg_obj = {
                "role": source_type.lower()
            }

            wrapper = [
                {
                    "type": "text",
                    "text": txt_content
                }
            ]

            if img_urls and source_type == HistoryBuilder.ChatRoles.USER:
                for img_url in img_urls:
                    uri = f"{img_url}"

                    try:
                        output = requests.get(uri)
                        data_bytes = output.content
                        image_b64 = b64.b64encode(data_bytes).decode("utf-8")

                    except Exception as e:
                        logger.error(f"Error while fetching image content: {e}")
                        continue

                    img_content_wrapper = {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{img_url.split('.')[-1]};base64,{image_b64}"
                        }
                    }

                    img_uri_wrapper = {
                        "type": "text",
                        "text": f"Detected Image URLs: {img_url}"
                    }

                    wrapper.append(img_content_wrapper)
                    wrapper.append(img_uri_wrapper)

            if f_urls and source_type == HistoryBuilder.ChatRoles.USER:
                for f_url in f_urls:
                    f_uri_info_wrapper = {
                        "type": "text",
                        "text": f"Detected File URLs: {f_url}"
                    }

                    wrapper.append(f_uri_info_wrapper)

            msg_obj["content"] = wrapper

            if source_type != HistoryBuilder.ChatRoles.SYSTEM:
                history.append(msg_obj)

            tx = LLMTransaction.objects.create(
                organization=lean_chat.organization,
                model=lean_chat.lean_assistant.llm_model,
                responsible_user=lean_chat.user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=txt_content,
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=source_type.lower(),
                transaction_source=lean_chat.chat_source
            )

            lean_chat.transactions.add(tx)

            lean_chat.save()

            logger.info(f"Lean Chat Transaction: {tx}")

            msg.save()

        history = ContextMemoryManager.handle_context_leanmod(
            chat_history=history,
            lean_assistant=lean_chat.lean_assistant
        )

        return history, temporary_uuid

    @staticmethod
    def build_voidforger(
        voidforger_chat: MultimodalVoidForgerChat
    ):

        from apps.core.generative_ai.utils import (
            GPT_DEFAULT_ENCODING_ENGINE
        )

        msgs = voidforger_chat.voidforger_chat_messages.all().order_by("sent_at")

        history = []

        temporary_uuid = uuid.uuid4()

        for msg in msgs:
            source_type = msg.sender_type

            if source_type == HistoryBuilder.ChatRoles.TOOL:
                source_type = HistoryBuilder.ChatRoles.ASSISTANT

            txt_content = msg.message_text_content

            img_urls = msg.message_image_contents
            f_urls = msg.message_file_contents

            msg_obj = {
                "role": source_type.lower()
            }

            wrapper = [
                {
                    "type": "text",
                    "text": txt_content
                }
            ]

            if img_urls and source_type == HistoryBuilder.ChatRoles.USER:
                for img_url in img_urls:
                    uri = f"{img_url}"

                    try:
                        output = requests.get(uri)
                        data_bytes = output.content
                        image_b64 = b64.b64encode(data_bytes).decode("utf-8")

                    except Exception as e:
                        logger.error(f"Error while fetching image content: {e}")
                        continue

                    img_content_wrapper = {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{img_url.split('.')[-1]};base64,{image_b64}"
                        }
                    }

                    img_uri_wrapper = {
                        "type": "text",
                        "text": f"Detected Image URLs: {img_url}"
                    }

                    wrapper.append(img_content_wrapper)
                    wrapper.append(img_uri_wrapper)

            if f_urls and source_type == HistoryBuilder.ChatRoles.USER:

                for f_url in f_urls:
                    f_uri_info_wrapper = {
                        "type": "text",
                        "text": f"Detected File URLs: {f_url}"
                    }

                    wrapper.append(f_uri_info_wrapper)

            msg_obj["content"] = wrapper

            if source_type != HistoryBuilder.ChatRoles.SYSTEM:
                history.append(msg_obj)

            tx = LLMTransaction.objects.create(
                organization=voidforger_chat.voidforger.llm_model.organization,
                model=voidforger_chat.voidforger.llm_model,
                responsible_user=voidforger_chat.user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_context_content=txt_content,
                llm_cost=0,
                internal_service_cost=0,
                tax_cost=0,
                total_cost=0,
                total_billable_cost=0,
                transaction_type=source_type.lower(),
                transaction_source=voidforger_chat.chat_source
            )

            voidforger_chat.transactions.add(tx)
            voidforger_chat.save()

            logger.info(f"VoidForger Chat Transaction: {tx}")
            msg.save()

        history = ContextMemoryManager.handle_context_voidforger(
            chat_history=history,
            voidforger=voidforger_chat.voidforger
        )

        return history, temporary_uuid
