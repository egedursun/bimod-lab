#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: expert_network_executor.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
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

from apps.core.expert_networks.prompts.build_expert_network_to_assistant_instructions_prompt import \
    build_leanmod_to_expert_assistant_instructions_prompt
from apps.core.expert_networks.prompts.error_messages import DEFAULT_EXPERT_ASSISTANT_ERROR_MESSAGE
from apps.assistants.models import Assistant
from apps.leanmod.models import ExpertNetwork, ExpertNetworkAssistantReference
from apps.multimodal_chat.models import MultimodalChat, MultimodalChatMessage
from apps.multimodal_chat.utils import SourcesForMultimodalChatsNames

logger = logging.getLogger(__name__)


class ExpertNetworkExecutor:
    def __init__(self, network):
        network: ExpertNetwork
        self.network = network

    def consult_by_query(
        self,
        reference: ExpertNetworkAssistantReference,
        query: str,
        image_urls=None,
        file_urls=None
    ):

        from apps.core.generative_ai.gpt_openai_manager import OpenAIGPTClientManager
        expert_agent: Assistant = reference.assistant
        structured_order = build_leanmod_to_expert_assistant_instructions_prompt(query_text=query)

        try:
            new_chat_object = MultimodalChat.objects.create(
                organization=expert_agent.organization,
                assistant=expert_agent,
                user=self.network.created_by_user,
                chat_source=SourcesForMultimodalChatsNames.ORCHESTRATION,
                is_archived=False,
                created_by_user_id=self.network.created_by_user.id
            )
            chat = new_chat_object
            logger.info(f"Created new chat object for expert network consultation: {chat}")

        except Exception as e:
            logger.error(f"Failed to create new chat object for expert network consultation: {e}")
            return DEFAULT_EXPERT_ASSISTANT_ERROR_MESSAGE

        try:
            llm_client = OpenAIGPTClientManager(
                assistant=expert_agent,
                chat_object=chat
            )

            logger.info(f"Created new OpenAI GPT client manager for expert network consultation: {llm_client}")
        except Exception as e:
            logger.error(f"Failed to create new OpenAI GPT client manager for expert network consultation: {e}")
            return DEFAULT_EXPERT_ASSISTANT_ERROR_MESSAGE

        if image_urls is not None:
            structured_order += """
                ---
                *IMAGE URLS*
            """
            for image_url in image_urls:
                structured_order += f"""
                - {image_url}
            """
            structured_order += "---"
        if file_urls is not None:
            structured_order += """
                *FILE URLS*
            """
            for file_url in file_urls:
                structured_order += f"""
                - {file_url}
            """
            structured_order += "---"

        MultimodalChatMessage.objects.create(
            multimodal_chat=chat,
            sender_type='USER',
            message_text_content=structured_order,
            message_image_contents=image_urls,
            message_file_contents=file_urls
        )

        output = llm_client.respond(
            latest_message=structured_order,
            image_uris=image_urls,
            file_uris=file_urls
        )

        MultimodalChatMessage.objects.create(
            multimodal_chat=chat,
            sender_type='ASSISTANT',
            message_text_content=output
        )

        logger.info(f"Created new chat message object for expert network consultation response: {output}")
        return output
