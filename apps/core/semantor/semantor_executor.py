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
from apps.core.expert_networks.prompts.build_expert_network_to_assistant_instructions_prompt import (
    build_leanmod_to_expert_assistant_instructions_prompt
)

from apps.core.expert_networks.prompts.error_messages import (
    DEFAULT_EXPERT_ASSISTANT_ERROR_MESSAGE
)

from apps.core.generative_ai.gpt_openai_manager import OpenAIGPTClientManager

from apps.core.generative_ai.utils import (
    ChatRoles,
    DEFAULT_ERROR_MESSAGE
)

from apps.core.semantor.utils import (
    VECTOR_INDEX_PATH_ASSISTANTS,
    OpenAIEmbeddingModels,
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS,
    VECTOR_INDEX_PATH_INTEGRATIONS,
    SEMANTOR_DEFAULT_SEARCH_RESULTS_ASSISTANTS,
    SEMANTOR_DEFAULT_SEARCH_RESULTS_INTEGRATIONS,
    SEMANTOR_DEFAULT_SEARCH_RESULTS_LEANMOD_ASSISTANTS,
    VECTOR_INDEX_PATH_LEANMOD_ASSISTANTS
)

from apps.core.system_prompts.system_prompt_factory_builder import SystemPromptFactoryBuilder

from apps.core.system_prompts.voidforger.helpers.error_messages import (
    DEFAULT_LEANMOD_ASSISTANT_ERROR_MESSAGE
)

from apps.core.system_prompts.voidforger.tools.voidforger_to_leanmod_assistant_instructions_prompt import (
    build_voidforger_to_leanmod_assistant_instructions_prompt
)

from apps.datasource_codebase.models import CodeRepositoryStorageConnection
from apps.datasource_file_systems.models import DataSourceFileSystem
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection
from apps.datasource_nosql.models import NoSQLDatabaseConnection
from apps.datasource_sql.models import SQLDatabaseConnection
from apps.hadron_prime.models import HadronNode
from apps.leanmod.models import LeanAssistant
from apps.llm_core.models import LLMCore
from apps.metakanban.models import MetaKanbanBoard
from apps.metatempo.models import MetaTempoConnection
from apps.mm_apis.models import CustomAPIReference
from apps.mm_functions.models import CustomFunctionReference
from apps.mm_scripts.models import CustomScriptReference

from apps.multimodal_chat.models import (
    MultimodalChat,
    MultimodalChatMessage,
    MultimodalLeanChat,
    MultimodalLeanChatMessage
)

from apps.multimodal_chat.utils import SourcesForMultimodalChatsNames
from apps.orchestrations.models import OrchestrationReactantAssistantConnection
from apps.projects.models import ProjectItem

from apps.semantor.models import (
    AssistantVectorData,
    IntegrationVectorData,
    LeanModVectorData,
    SemantorConfiguration
)

logger = logging.getLogger(__name__)


class SemantorVectorSearchExecutionManager:
    def __init__(
        self,
        user: User,
        llm_model: LLMCore,
        vector_dim: int = OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
    ):
        self.user: User = user
        self.llm_model: LLMCore = llm_model
        self.vector_dim = vector_dim
        self.assistants_index_path = os.path.join(
            VECTOR_INDEX_PATH_ASSISTANTS, f'assistants_index_{self.llm_model.organization.id}.index')
        self.leanmod_assistants_index_path = os.path.join(
            VECTOR_INDEX_PATH_LEANMOD_ASSISTANTS, f'leanmod_assistants_index_{self.llm_model.organization.id}.index')
        self.integrations_index_path = os.path.join(
            VECTOR_INDEX_PATH_INTEGRATIONS, f"integrations_index.index")

        if os.path.exists(self.assistants_index_path):
            self.assistants_index = faiss.read_index(self.assistants_index_path)
        else:
            self.assistants_index = faiss.IndexIDMap(faiss.IndexFlatL2(self.vector_dim))
            faiss.write_index(self.assistants_index, self.assistants_index_path)

        if os.path.exists(self.leanmod_assistants_index_path):
            self.leanmod_assistants_index = faiss.read_index(self.leanmod_assistants_index_path)
        else:
            self.leanmod_assistants_index = faiss.IndexIDMap(faiss.IndexFlatL2(self.vector_dim))
            faiss.write_index(self.leanmod_assistants_index, self.leanmod_assistants_index_path)

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
            structured_order = build_leanmod_to_expert_assistant_instructions_prompt(
                query_text=query,
            )
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

            structured_order = build_leanmod_to_expert_assistant_instructions_prompt(
                query_text=query
            )
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

            try:
                semantor_config: SemantorConfiguration = SemantorConfiguration.objects.get(user=self.user)
                if semantor_config is None:
                    semantor_config = SemantorConfiguration.objects.create(user=self.user)
            except Exception as e:
                logger.error(f"Failed to retrieve Semantor configuration: {e}")
                return DEFAULT_EXPERT_ASSISTANT_ERROR_MESSAGE

            temporary_data_source_and_tool_access = semantor_config.temporary_data_source_and_tool_access
            temporary_sources = {}
            if temporary_data_source_and_tool_access is True:
                temporary_sources = self._gather_temporary_sources(temporary_assistant)

            system_prompt = SystemPromptFactoryBuilder.build_semantor(
                assistant_name=temporary_assistant.name,
                instructions=temporary_assistant.instructions,
                tone=temporary_assistant.tone,
                audience=temporary_assistant.audience,
                language=temporary_assistant.response_language,
                chat_name="Consultation Chat",
                temporary_sources=temporary_sources
            )

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

            logger.info(
                f"Created temporary chat message object for Semantor network consultation response: {choice_message_content}")
            return choice_message_content

    def search_leanmod_assistants(self, query: str,
                                  n_results: int = SEMANTOR_DEFAULT_SEARCH_RESULTS_LEANMOD_ASSISTANTS) -> List[Dict]:
        query_vector = np.array([self._generate_query_embedding(query)], dtype=np.float32)
        if self.leanmod_assistants_index is None:
            raise ValueError("[search_assistants] FAISS index not initialized or loaded properly.")

        distances, ids = self.leanmod_assistants_index.search(query_vector, n_results)
        results = []
        for item_id, distance in zip(ids[0], distances[0]):
            if item_id == -1:
                continue
            try:
                instance = LeanModVectorData.objects.get(id=item_id)
                results.append({
                    "id": instance.id,
                    "data": instance.raw_data,
                    "distance": distance,
                })
            except LeanModVectorData.DoesNotExist:
                print(f"Warning: LeanMod Assistant Instance with ID {item_id} not found in the vector database.")
                logger.error(f"LeanMod Assistant Instance with ID {item_id} not found in the vector database.")

        return results

    def consult_leanmod_oracle_by_query(
        self, consultation_object_id: int,
        query: str,
        image_urls=None,
        file_urls=None
    ):
        from apps.core.generative_ai.gpt_openai_manager_lean import OpenAIGPTLeanClientManager
        leanmod_oracle_vector: LeanModVectorData = LeanModVectorData.objects.get(id=consultation_object_id)
        lean_assistant: LeanAssistant = leanmod_oracle_vector.leanmod_assistant
        structured_order = build_voidforger_to_leanmod_assistant_instructions_prompt(query_text=query)
        try:
            new_chat_object = MultimodalLeanChat.objects.create(
                organization=lean_assistant.organization, lean_assistant=lean_assistant,
                user=self.llm_model.created_by_user, chat_source=SourcesForMultimodalChatsNames.ORCHESTRATION,
                is_archived=False, created_by_user_id=self.llm_model.created_by_user.id)
            chat = new_chat_object
            logger.info(f"Created new chat object for VoidForger to LeanMod Oracle consultation: {chat}")
        except Exception as e:
            logger.error(f"Failed to create new chat object for VoidForger to LeanMod Oracle consultation: {e}")
            return DEFAULT_LEANMOD_ASSISTANT_ERROR_MESSAGE

        try:
            llm_client: OpenAIGPTLeanClientManager = OpenAIGPTLeanClientManager(assistant=lean_assistant,
                                                                                multimodal_chat=chat, user=self.user)
            logger.info(
                f"Created new OpenAI GPT Lean client manager for VoidForger to LeanMod Oracle consultation: {llm_client}")
        except Exception as e:
            logger.error(
                f"Failed to create new OpenAI GPT Lean client manager for VoidForger to LeanMod Oracle consultation: {e}")
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

        MultimodalLeanChatMessage.objects.create(
            multimodal_lean_chat=chat, sender_type='USER', message_text_content=structured_order,
            message_image_contents=image_urls, message_file_contents=file_urls)

        output = llm_client.respond(
            latest_message=structured_order, image_uris=image_urls, file_uris=file_urls)

        MultimodalLeanChatMessage.objects.create(
            multimodal_lean_chat=chat, sender_type='ASSISTANT', message_text_content=output)
        logger.info(
            f"Created new chat message object for VoidForger to LeanMod Oracle consultation response: {output}")
        return output

    def _gather_temporary_sources(self, temporary_assistant):
        source_references = {
            "tools": {
                "image_generation_capability": False,
                "time_awareness": False,
                "place_awareness": False,
                "reasoning_capability_choice": "N/A",
                "functions": [],
                "apis": [],
                "scripts": [],
            },
            "data_sources": {
                "browsers": {},
                "file_systems": {},
                "sql_dbs": {},
                "nosql_dbs": {},
                "knowledge_bases": {},
                "codebases": {},
                "media_storages": {},
                "ml_storages": {},
                "projects": {},
                "video_generators": {},
                "hadron_node_connections": {},
                "metakanban_board_connections": {},
                "metatempo_tracker_connections": {},
                "orchestration_trigger_connections": {},
            },
        }
        reference_assistants = Assistant.objects.filter(organization__in=[temporary_assistant.organization])

        data_source__browsers = []
        data_source__file_systems = []
        data_source__sql_dbs = []
        data_source__nosql_dbs = []
        data_source__knowledge_bases = []
        data_source__codebases = []
        data_source__media_storages = []
        data_source__ml_storages = []
        data_source__projects = []
        data_source__video_generators = []
        data_source__hadron_node_connections = []
        data_source__metakanban_board_connections = []
        data_source__metatempo_tracker_connections = []
        data_source__orchestration_trigger_connections = []

        tools__functions = []
        tools__apis = []
        tools__scripts = []

        for assistant in reference_assistants:
            assistant: Assistant

            assistant__data_source__browsers = assistant.datasourcebrowserconnection_set.all()
            if len(assistant__data_source__browsers) > 0:
                data_source__browsers.append(assistant__data_source__browsers[0])

            assistant__data_source__file_systems = assistant.data_source_file_systems.all()
            fs_recorded_hosts = []
            fs_recorded_count = 0
            for file_system in assistant__data_source__file_systems:
                file_system: DataSourceFileSystem
                if fs_recorded_count == 5:
                    break
                if file_system.host_url not in fs_recorded_hosts:
                    data_source__file_systems.append(file_system)
                    fs_recorded_hosts.append(file_system.host_url)
                    fs_recorded_count += 1
            ######
            source_references["data_sources"]["file_systems"] = data_source__file_systems
            pass

            assistant__data_source__sql_dbs = assistant.sql_database_connections.all()
            sql_recorded_hosts, sql_recorded_db_names = [], []
            sql_recorded_count = 0
            for sql_db in assistant__data_source__sql_dbs:
                sql_db: SQLDatabaseConnection
                if sql_recorded_count == 5:
                    break
                if sql_db.host not in sql_recorded_hosts and sql_db.database_name not in sql_recorded_db_names:
                    data_source__sql_dbs.append(sql_db)
                    sql_recorded_hosts.append(sql_db.host)
                    sql_recorded_db_names.append(sql_db.database_name)
                    sql_recorded_count += 1
            ######
            source_references["data_sources"]["sql_dbs"] = data_source__sql_dbs
            pass

            assistant__data_source__nosql_dbs = assistant.nosql_database_connections.all()
            nosql_recorded_hosts, nosql_recorded_bucket_names = [], []
            nosql_recorded_count = 0
            for nosql_db in assistant__data_source__nosql_dbs:
                nosql_db: NoSQLDatabaseConnection
                if nosql_recorded_count == 5:
                    break
                if nosql_db.host not in nosql_recorded_hosts and nosql_db.bucket_name not in nosql_recorded_bucket_names:
                    data_source__nosql_dbs.append(nosql_db)
                    nosql_recorded_hosts.append(nosql_db.host)
                    nosql_recorded_bucket_names.append(nosql_db.bucket_name)
                    nosql_recorded_count += 1
            ######
            source_references["data_sources"]["nosql_dbs"] = data_source__nosql_dbs
            pass

            assistant__data_source__knowledge_bases = assistant.documentknowledgebaseconnection_set.all()
            kb_recorded_hosts = []
            kb_recorded_count = 0
            for kb in assistant__data_source__knowledge_bases:
                kb: DocumentKnowledgeBaseConnection
                if kb_recorded_count == 5:
                    break
                if kb.host_url not in kb_recorded_hosts:
                    data_source__knowledge_bases.append(kb)
                    kb_recorded_hosts.append(kb.host_url)
                    kb_recorded_count += 1
            ######
            source_references["data_sources"]["knowledge_bases"] = data_source__knowledge_bases
            pass

            assistant__data_source__codebases = assistant.coderepositorystorageconnection_set.all()
            cb_recorded_hosts = []
            cb_recorded_count = 0
            for cb in assistant__data_source__codebases:
                cb: CodeRepositoryStorageConnection
                if cb_recorded_count == 5:
                    break
                if cb.host_url not in cb_recorded_hosts:
                    data_source__codebases.append(cb)
                    cb_recorded_hosts.append(cb.host_url)
                    cb_recorded_count += 1
            ######
            source_references["data_sources"]["codebases"] = data_source__codebases
            pass

            assistant__data_source__media_storages = assistant.datasourcemediastorageconnection_set.all()
            recorded_media_storage_categories = []
            for media_storage in assistant__data_source__media_storages:
                media_storage: DataSourceMediaStorageConnection
                if media_storage.media_category not in recorded_media_storage_categories:
                    data_source__media_storages.append(media_storage)
                    recorded_media_storage_categories.append(media_storage.media_category)
            ######
            source_references["data_sources"]["media_storages"] = data_source__media_storages
            pass

            assistant__data_source__ml_storages = assistant.datasourcemlmodelconnection_set.all()
            if len(assistant__data_source__ml_storages) > 0:
                data_source__ml_storages.append(assistant__data_source__ml_storages[0])

            assistant__data_source__projects = assistant.project_items.all()
            recorded_project_ids = []
            recorded_project_count = 0
            for project in assistant__data_source__projects:
                project: ProjectItem
                if recorded_project_count == 5:
                    break
                if project.id not in recorded_project_ids:
                    data_source__projects.append(project)
                    recorded_project_ids.append(project.id)
                    recorded_project_count += 1
            ######
            source_references["data_sources"]["projects"] = data_source__projects
            pass

            assistant__data_source__video_generators = assistant.videogeneratorconnection_set.all()
            if len(assistant__data_source__video_generators) > 0:
                data_source__video_generators.append(assistant__data_source__video_generators[0])
            ######
            source_references["data_sources"]["video_generators"] = data_source__video_generators
            pass

            assistant__data_source__hadron_node_connections = assistant.hadronnodeassistantconnection_set.all()
            recorded_hadron_node_ids = []
            recorded_hadron_node_count = 0
            for hadron_node in assistant__data_source__hadron_node_connections:
                hadron_node: HadronNode
                if recorded_hadron_node_count == 5:
                    break
                if hadron_node.id not in recorded_hadron_node_ids:
                    data_source__hadron_node_connections.append(hadron_node)
                    recorded_hadron_node_ids.append(hadron_node.id)
                    recorded_hadron_node_count += 1
            ######
            source_references["data_sources"]["hadron_node_connections"] = data_source__hadron_node_connections
            pass

            assistant__data_source__metakanban_board_connections = assistant.metakanbanassistantconnection_set.all()
            recorded_metakanban_boards = []
            recorded_metakanban_count = 0
            for metakanban_board in assistant__data_source__metakanban_board_connections:
                metakanban_board: MetaKanbanBoard
                if recorded_metakanban_count == 5:
                    break
                if metakanban_board.id not in recorded_metakanban_boards:
                    data_source__metakanban_board_connections.append(metakanban_board)
                    recorded_metakanban_boards.append(metakanban_board.id)
                    recorded_metakanban_count += 1
            ######
            source_references["data_sources"][
                "metakanban_board_connections"] = data_source__metakanban_board_connections
            pass

            recorded_metatempo_connections = []
            recorded_metatempo_count = 0
            if len(assistant__data_source__metakanban_board_connections) > 0:
                for metakanban_board in assistant__data_source__metakanban_board_connections:
                    if recorded_metatempo_count == 5:
                        break
                    metatempo_tracker: MetaTempoConnection = MetaTempoConnection.objects.get(
                        metakanban_board=metakanban_board
                    )
                    if metatempo_tracker.id not in recorded_metatempo_connections:
                        data_source__metatempo_tracker_connections.append(metatempo_tracker)
                        recorded_metatempo_connections.append(metatempo_tracker.id)
                        recorded_metatempo_count += 1
            ######
            source_references["data_sources"][
                "metatempo_tracker_connections"] = data_source__metatempo_tracker_connections
            pass

            assistant__data_source__orchestration_trigger_connections = assistant.orchestrationreactantassistantconnection_set.all()
            recorded_orchestration_triggers = []
            recorded_orchestration_count = 0
            for orchestration_trigger in assistant__data_source__orchestration_trigger_connections:
                orchestration_trigger: OrchestrationReactantAssistantConnection
                if recorded_orchestration_count == 5:
                    break
                if orchestration_trigger.id not in recorded_orchestration_triggers:
                    data_source__orchestration_trigger_connections.append(orchestration_trigger)
                    recorded_orchestration_triggers.append(orchestration_trigger.id)
                    recorded_orchestration_count += 1
            ######
            source_references["data_sources"][
                "orchestration_trigger_connections"] = data_source__orchestration_trigger_connections
            pass

            ##############################

            assistant__tool__image_generation_capability = assistant.image_generation_capability
            tools__image_generation_capability = assistant__tool__image_generation_capability
            ######
            source_references["tools"]["image_generation_capability"] = tools__image_generation_capability
            pass

            assistant__tool__time_awareness = assistant.time_awareness
            tools__time_awareness = assistant__tool__time_awareness
            ######
            source_references["tools"]["time_awareness"] = tools__time_awareness
            pass

            assistant__tool__place_awareness = assistant.place_awareness
            tools__place_awareness = assistant__tool__place_awareness
            ######
            source_references["tools"]["place_awareness"] = tools__place_awareness
            pass

            assistant__tool__reasoning_capability_choice = assistant.multi_step_reasoning_capability_choice
            tools__reasoning_capability_choice = assistant__tool__reasoning_capability_choice
            ######
            source_references["tools"]["reasoning_capability_choice"] = tools__reasoning_capability_choice
            pass

            assistant__tool__functions = assistant.customfunctionreference_set.all()
            recorded_function__reference_ids = []
            recorded_function_count = 0
            for function_ref in assistant__tool__functions:
                function_ref: CustomFunctionReference
                if recorded_function_count == 5:
                    break
                if function_ref.custom_function.id not in recorded_function__reference_ids:
                    tools__functions.append(function_ref)
                    recorded_function__reference_ids.append(function_ref.custom_function.id)
                    recorded_function_count += 1
            ######
            source_references["tools"]["functions"] = tools__functions
            pass

            assistant__tool__apis = assistant.customapireference_set.all()
            recorded_api__reference_ids = []
            recorded_api_count = 0
            for api_ref in assistant__tool__apis:
                api_ref: CustomAPIReference
                if recorded_api_count == 5:
                    break
                if api_ref.custom_api.id not in recorded_api__reference_ids:
                    tools__apis.append(api_ref)
                    recorded_api__reference_ids.append(api_ref.custom_api.id)
                    recorded_api_count += 1
            ######
            source_references["tools"]["apis"] = tools__apis
            pass

            assistant__tool__scripts = assistant.customscriptreference_set.all()
            recorded_script__reference_ids = []
            recorded_script_count = 0
            for script_ref in assistant__tool__scripts:
                script_ref: CustomScriptReference
                if recorded_script_count == 5:
                    break
                if script_ref.custom_script.id not in recorded_script__reference_ids:
                    tools__scripts.append(script_ref)
                    recorded_script__reference_ids.append(script_ref.custom_script.id)
                    recorded_script_count += 1
            ######
            source_references["tools"]["scripts"] = tools__scripts
            pass

        return source_references
