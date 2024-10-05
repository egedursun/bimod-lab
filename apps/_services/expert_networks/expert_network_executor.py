#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#

from apps._services.expert_networks.prompts.build_expert_network_to_assistant_instructions_prompt import \
    build_leanmod_to_expert_assistant_instructions_prompt
from apps._services.expert_networks.prompts.error_messages import DEFAULT_EXPERT_ASSISTANT_ERROR_MESSAGE
from apps.assistants.models import Assistant
from apps.leanmod.models import ExpertNetwork, ExpertNetworkAssistantReference
from apps.multimodal_chat.models import MultimodalChat, MultimodalChatMessage
from apps.multimodal_chat.utils import ChatSourcesNames


class ExpertNetworkExecutor:
    def __init__(self, network):
        network: ExpertNetwork
        self.network = network

    def consult_by_query(self, reference: ExpertNetworkAssistantReference, query: str, image_urls=None,
                         file_urls=None):
        print(f"[ExpertNetworkExecutor.consult_by_query] Executing the query: {query}")
        print(f"[ExpertNetworkExecutor.consult_by_query] Image URLs: {image_urls}")
        print(f"[ExpertNetworkExecutor.consult_by_query] File URLs: {file_urls}")
        from apps._services.llms.openai import InternalOpenAIClient
        expert_assistant: Assistant = reference.assistant

        # i. Build the 'instructions' and include 'query' in it
        structured_order = build_leanmod_to_expert_assistant_instructions_prompt(query_text=query)

        try:
            new_chat_object = MultimodalChat.objects.create(
                organization=expert_assistant.organization,
                assistant=expert_assistant,
                user=self.network.created_by_user,
                chat_source=ChatSourcesNames.ORCHESTRATION,
                is_archived=False,
                created_by_user_id=self.network.created_by_user.id
            )
            chat = new_chat_object
        except Exception as e:
            print(f"[ExpertNetworkExecutor.consult_by_query] Error while creating the chat object: {e}")
            return DEFAULT_EXPERT_ASSISTANT_ERROR_MESSAGE

        try:
            internal_llm_client = InternalOpenAIClient(
                assistant=expert_assistant,
                multimodal_chat=chat,
            )
        except Exception as e:
            print(f"[ExpertNetworkExecutor.consult_by_query] Error while setting the connection and user: {e}")
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
            multimodal_chat=chat, sender_type='USER', message_text_content=structured_order,
            message_image_contents=image_urls, message_file_contents=file_urls
        )
        print(f"[ExpertNetworkExecutor.consult_by_query] Structured order: {structured_order}")
        final_response = internal_llm_client.respond(
            latest_message=structured_order,
            image_uris=image_urls,
            file_uris=file_urls
        )
        MultimodalChatMessage.objects.create(
            multimodal_chat=chat, sender_type='ASSISTANT', message_text_content=final_response
        )

        # vi. Return the final response of the assistant as text
        return final_response
