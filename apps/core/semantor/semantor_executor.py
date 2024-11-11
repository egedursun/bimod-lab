#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: semantor_executor.py
#  Last Modified: 2024-11-09 17:10:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-09 17:10:41
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
import os

import faiss
import numpy as np
from typing import List, Dict

import requests
from django.contrib.auth.models import User

from apps.assistants.models import Assistant
from apps.core.expert_networks.prompts.build_expert_network_to_assistant_instructions_prompt import \
    build_leanmod_to_expert_assistant_instructions_prompt
from apps.core.expert_networks.prompts.error_messages import DEFAULT_EXPERT_ASSISTANT_ERROR_MESSAGE
from apps.core.generative_ai.gpt_openai_manager import OpenAIGPTClientManager
from apps.core.generative_ai.utils import ChatRoles, DEFAULT_ERROR_MESSAGE
from apps.core.semantor.utils import VECTOR_INDEX_PATH_ASSISTANTS, OpenAIEmbeddingModels, \
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS, VECTOR_INDEX_PATH_INTEGRATIONS
from apps.core.system_prompts.system_prompt_factory_builder import SystemPromptFactoryBuilder
from apps.llm_core.models import LLMCore
from apps.multimodal_chat.models import MultimodalChat, MultimodalChatMessage
from apps.multimodal_chat.utils import SourcesForMultimodalChatsNames
from apps.semantor.models import AssistantVectorData, IntegrationVectorData

logger = logging.getLogger(__name__)

SEMANTOR_DEFAULT_SEARCH_RESULTS_ASSISTANTS = 5
SEMANTOR_DEFAULT_SEARCH_RESULTS_INTEGRATIONS = 5


class SemantorVectorSearchExecutionManager:
    def __init__(self, user: User, llm_model: LLMCore, vector_dim: int = OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS):
        self.user: User = user
        self.llm_model: LLMCore = llm_model
        self.vector_dim = vector_dim
        self.assistants_index_path = os.path.join(
            VECTOR_INDEX_PATH_ASSISTANTS, f'assistants_index_{self.llm_model.organization.id}.index')
        self.integrations_index_path = os.path.join(
            VECTOR_INDEX_PATH_INTEGRATIONS, f"integrations_index.index")

        if os.path.exists(self.assistants_index_path):
            self.assistants_index = faiss.read_index(self.assistants_index_path)
        else:
            self.assistants_index = faiss.IndexIDMap(faiss.IndexFlatL2(self.vector_dim))
            faiss.write_index(self.assistants_index, self.assistants_index_path)

        if os.path.exists(self.integrations_index_path):
            self.integrations_index = faiss.read_index(self.integrations_index_path)
        else:
            self.integrations_index = faiss.IndexIDMap(faiss.IndexFlatL2(self.vector_dim))
            faiss.write_index(self.integrations_index, self.integrations_index_path)

    def _generate_query_embedding(self, query: str) -> List[float]:
        c = OpenAIGPTClientManager.get_naked_client(llm_model=self.llm_model)
        response = c.embeddings.create(input=query, model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE)
        return response.data[0].embedding

    def search_assistants(self, query: str, n_results: int = SEMANTOR_DEFAULT_SEARCH_RESULTS_ASSISTANTS) -> List[Dict]:
        query_vector = np.array([self._generate_query_embedding(query)], dtype=np.float32)
        if self.assistants_index is None:
            raise ValueError("[search_assistants] FAISS index not initialized or loaded properly.")

        distances, ids = self.assistants_index.search(query_vector, n_results)
        results = []
        for item_id, distance in zip(ids[0], distances[0]):
            if item_id == -1:
                continue
            try:
                instance = AssistantVectorData.objects.get(id=item_id)
                results.append({
                    "id": instance.id,
                    "data": instance.raw_data,
                    "distance": distance,
                })
            except AssistantVectorData.DoesNotExist:
                print(f"Warning: Assistant Instance with ID {item_id} not found in the vector database.")
                logger.error(f"Assistant Instance with ID {item_id} not found in the vector database.")

        return results

    def search_integrations(self, query: str, n_results: int = SEMANTOR_DEFAULT_SEARCH_RESULTS_INTEGRATIONS) -> List[
        Dict]:
        query_vector = np.array([self._generate_query_embedding(query)], dtype=np.float32)
        if self.integrations_index is None:
            raise ValueError("[search_integrations] FAISS index not initialized or loaded properly.")

        distances, ids = self.integrations_index.search(query_vector, n_results)
        results = []
        for item_id, distance in zip(ids[0], distances[0]):
            if item_id == -1:
                continue
            try:
                instance = IntegrationVectorData.objects.get(id=item_id)
                results.append({
                    "id": instance.id,
                    "data": instance.raw_data,
                    "distance": distance,
                })
            except IntegrationVectorData.DoesNotExist:
                print(f"Warning: Integration Instance with ID {item_id} not found in the vector database.")
                logger.error(f"Integration Instance with ID {item_id} not found in the vector database.")

        return results

    def consult_semantor_by_query(
        self, consultation_object_id: int,
        query: str,
        is_local: bool = True,
        image_urls=None,
        file_urls=None
    ):
        from apps.core.generative_ai.gpt_openai_manager import OpenAIGPTClientManager

        if is_local:
            expert_agent_vector: AssistantVectorData = AssistantVectorData.objects.get(id=consultation_object_id)
            expert_agent: Assistant = expert_agent_vector.assistant
            structured_order = build_leanmod_to_expert_assistant_instructions_prompt(query_text=query)
            try:
                new_chat_object = MultimodalChat.objects.create(
                    organization=expert_agent.organization, assistant=expert_agent,
                    user=self.llm_model.created_by_user, chat_source=SourcesForMultimodalChatsNames.ORCHESTRATION,
                    is_archived=False, created_by_user_id=self.llm_model.created_by_user.id)
                chat = new_chat_object
                logger.info(f"Created new chat object for Semantor Network consultation: {chat}")
            except Exception as e:
                logger.error(f"Failed to create new chat object for Semantor Network consultation: {e}")
                return DEFAULT_EXPERT_ASSISTANT_ERROR_MESSAGE

            try:
                llm_client = OpenAIGPTClientManager(assistant=expert_agent, chat_object=chat)
                logger.info(f"Created new OpenAI GPT client manager for Semantor network consultation: {llm_client}")
            except Exception as e:
                logger.error(f"Failed to create new OpenAI GPT client manager for Semantor network consultation: {e}")
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
                message_image_contents=image_urls, message_file_contents=file_urls)
            output = llm_client.respond(
                latest_message=structured_order, image_uris=image_urls, file_uris=file_urls)

            MultimodalChatMessage.objects.create(
                multimodal_chat=chat, sender_type='ASSISTANT', message_text_content=output)
            logger.info(f"Created new chat message object for Semantor network consultation response: {output}")
            return output

        else:
            expert_integration_vector: IntegrationVectorData = IntegrationVectorData.objects.get(
                id=consultation_object_id)
            integration_data = expert_integration_vector.integration_assistant
            structured_order = build_leanmod_to_expert_assistant_instructions_prompt(query_text=query)
            temporary_assistant = Assistant(
                id=0,
                organization=self.llm_model.organization,
                llm_model=self.llm_model,
                name=integration_data.integration_name,
                description=integration_data.integration_description,
                instructions=integration_data.integration_instructions,
                response_template=integration_data.integration_response_template,
                audience=integration_data.integration_audience,
                tone=integration_data.integration_tone,
                assistant_image=integration_data.integration_assistant_image,
                max_retry_count=integration_data.integration_max_retries,
                tool_max_attempts_per_instance=integration_data.integration_max_tool_retries,
                tool_max_chains=integration_data.integration_max_tool_pipelines,
                max_context_messages=integration_data.integration_max_message_memory,
                time_awareness=integration_data.integration_time_awareness,
                place_awareness=integration_data.integration_location_awareness,
                multi_step_reasoning_capability_choice=integration_data.integration_multi_step_reasoning,
                image_generation_capability=integration_data.integration_image_generation_capability,
                context_overflow_strategy=integration_data.integration_context_overflow_strategy,
                response_language=integration_data.integration_response_language,
                glossary=integration_data.integration_glossary,
                ner_integration=integration_data.ner_integration,
                created_by_user=self.user,
                last_updated_by_user=self.user,
            )

            try:
                temporary_chat_object = MultimodalChat(
                    organization=temporary_assistant.organization, assistant=temporary_assistant,
                    user=self.llm_model.created_by_user, chat_source=SourcesForMultimodalChatsNames.ORCHESTRATION,
                    is_archived=False, created_by_user_id=self.llm_model.created_by_user.id)
                chat = temporary_chat_object
                logger.info(f"Created temporary chat object for Semantor Network consultation: {chat}")
            except Exception as e:
                logger.error(f"Failed to create temporary chat object for Semantor Network consultation: {e}")
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

            system_prompt = SystemPromptFactoryBuilder.build_lean(
                assistant_name=temporary_assistant.name, instructions=temporary_assistant.instructions,
                tone=temporary_assistant.tone, audience=temporary_assistant.audience,
                language=temporary_assistant.response_language, chat_name="Consultation Chat")

            query_prompt = {"role": ChatRoles.USER}
            wrapper = [{"type": "text", "text": structured_order}]
            for img_url in image_urls:
                uri = f"{img_url}"
                try:
                    output = requests.get(uri)
                    data_bytes = output.content
                    image_b64 = base64.b64encode(data_bytes).decode("utf-8")
                except Exception as e:
                    logger.error(f"Error while fetching image content: {e}")
                    continue
                img_wrapper = {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/{img_url.split('.')[-1]};base64,{image_b64}"}
                }
                img_uri_wrapper = {"type": "text", "text": f"Detected Image URLs: {img_url}"}
                wrapper.append(img_wrapper)
                wrapper.append(img_uri_wrapper)

            for f_url in file_urls:
                file_uri_info_wrapper = {"type": "text", "text": f"Detected File URLs: {f_url}"}
                wrapper.append(file_uri_info_wrapper)
            query_prompt["content"] = wrapper

            prompt_history = [system_prompt, query_prompt]
            naked_client = OpenAIGPTClientManager.get_naked_client(llm_model=self.llm_model)
            try:
                llm_output = naked_client.chat.completions.create(
                    model=self.llm_model.model_name, messages=prompt_history,
                    temperature=float(self.llm_model.temperature),
                    frequency_penalty=float(self.llm_model.frequency_penalty),
                    presence_penalty=float(self.llm_model.presence_penalty),
                    max_tokens=int(self.llm_model.maximum_tokens),
                    top_p=float(self.llm_model.top_p))
            except Exception as e:
                logger.error(f"Error occurred while retrieving the response from the language model: {str(e)}")
                return DEFAULT_ERROR_MESSAGE
            try:
                choices = llm_output.choices
                first_choice = choices[0]
                choice_message = first_choice.message
                choice_message_content = choice_message.content
            except Exception as e:
                logger.error(f"Error occurred while processing the response from the language model: {str(e)}")
                return DEFAULT_ERROR_MESSAGE

            logger.info(f"Created temporary chat message object for Semantor network consultation response: {choice_message_content}")
            return choice_message_content
