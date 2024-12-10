#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: chat_context_manager.py
#  Last Modified: 2024-10-05 02:13:34
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
import os
from typing import List, Dict

import faiss
import numpy as np

from apps.core.context_memory_manager.utils import (
    get_error_on_context_memory_handling_log,
    ASSISTANT_DEFAULT_SEARCH_RESULTS_OLD_CHAT_MESSAGES,
    LEANMOD_ASSISTANT_DEFAULT_SEARCH_RESULTS_OLD_CHAT_MESSAGES
)

from apps.core.semantor.utils import (
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS,
    OpenAIEmbeddingModels
)

from apps.core.system_prompts.chat_history_memory.build_chat_history_memory_instruction import (
    build_chat_history_memory_handling_prompt,
    build_chat_history_memory_stop_communication_handler_prompt
)

from apps.assistants.models import (
    Assistant,
    AssistantOldChatMessagesVectorData
)

from apps.assistants.utils import (
    ContextManagementStrategyNames,
    VECTOR_INDEX_PATH_ASSISTANT_CHAT_MESSAGES
)

from apps.leanmod.models import (
    LeanAssistant,
    LeanModOldChatMessagesVectorData
)

from apps.leanmod.utils import (
    VECTOR_INDEX_PATH_LEANMOD_CHAT_MESSAGES
)

from apps.multimodal_chat.models import (
    MultimodalChat,
    MultimodalLeanChat
)
from apps.voidforger.models import VoidForger

logger = logging.getLogger(__name__)


class ContextMemoryManager:
    @staticmethod
    def forget_oldest_chat_messages(
        message_history,
        maximum_allowed_messages
    ):
        from apps.core.generative_ai.utils import (
            ChatRoles
        )

        try:
            system_prompt = build_chat_history_memory_handling_prompt()

            logger.info(f"[ChatContextManager.forget_oldest_chat_messages] System prompt: {system_prompt}")

        except Exception as e:
            system_prompt = get_error_on_context_memory_handling_log(error_log=str(e))

            logger.error(f"[ChatContextManager.forget_oldest_chat_messages] Error creating system prompt: {e}")

        msg = {
            "role": ChatRoles.SYSTEM,
            "content": system_prompt
        }

        len_msg_history = len(message_history)

        if len_msg_history > maximum_allowed_messages:
            trimmed_msg_history = message_history[-maximum_allowed_messages:] + [msg]

            return trimmed_msg_history

        else:

            return message_history

    @staticmethod
    def stop_communication_at_threshold(
        message_history: list,
        maximum_allowed_messages
    ):
        from apps.core.generative_ai.utils import (
            ChatRoles
        )

        try:
            system_prompt = build_chat_history_memory_stop_communication_handler_prompt()

            logger.info(f"[ChatContextManager.stop_communication_at_threshold] System prompt: {system_prompt}")

        except Exception as e:
            logger.error(f"[ChatContextManager.stop_communication_at_threshold] Error creating system prompt: {e}")

            system_prompt = get_error_on_context_memory_handling_log(error_log=str(e))

        len_msg_history = len(message_history)

        if len_msg_history > maximum_allowed_messages:
            msg = {
                "role": ChatRoles.SYSTEM,
                "content": system_prompt
            }

            trimmed_msg_history = message_history[-maximum_allowed_messages:] + [msg]

            return trimmed_msg_history

        else:

            return message_history

    @staticmethod
    def store_context_memory_as_embedding(
        message_history,
        maximum_allowed_messages
    ):

        ############################################################################################################
        ############################################################################################################
        # The Django ORM data model automatically handles the Vectorization operations.
        #   - The embeddings and indexes are created and stored in the database, so no additional operation here.
        ############################################################################################################
        ############################################################################################################

        chat_history_length = len(message_history)

        if chat_history_length > maximum_allowed_messages:
            trimmed_msgs_history = message_history[-maximum_allowed_messages:]

        else:
            trimmed_msgs_history = message_history

        return trimmed_msgs_history

    @staticmethod
    def handle_context(
        chat_history,
        assistant: Assistant
    ):
        mgm_strategy = assistant.context_overflow_strategy
        max_context_msgs = assistant.max_context_messages

        if mgm_strategy == ContextManagementStrategyNames.FORGET:
            ctx_msgs = ContextMemoryManager._handle_strategy_forget_oldest(
                chat_history,
                max_context_msgs
            )

        elif mgm_strategy == ContextManagementStrategyNames.STOP:
            ctx_msgs = ContextMemoryManager._handle_strategy_stop_conversation(
                chat_history,
                max_context_msgs
            )

        elif mgm_strategy == ContextManagementStrategyNames.VECTORIZE:
            ctx_msgs = ContextMemoryManager._handle_strategy_vectorize_history(
                chat_history,
                max_context_msgs
            )

        else:
            ctx_msgs = ContextMemoryManager._handle_strategy_forget_oldest(
                chat_history,
                max_context_msgs
            )

        logger.info(f"[ChatContextManager.handle_context] Handled the context for Assistant.")

        return ctx_msgs

    @staticmethod
    def handle_context_leanmod(
        chat_history,
        lean_assistant: LeanAssistant
    ):

        mgm_strategy = lean_assistant.context_overflow_strategy
        max_context_msgs = lean_assistant.max_context_messages

        if mgm_strategy == ContextManagementStrategyNames.FORGET:
            ctx_msgs = ContextMemoryManager._handle_strategy_forget_oldest(
                chat_history,
                max_context_msgs
            )

        elif mgm_strategy == ContextManagementStrategyNames.STOP:
            ctx_msgs = ContextMemoryManager._handle_strategy_stop_conversation(
                chat_history,
                max_context_msgs
            )

        elif mgm_strategy == ContextManagementStrategyNames.VECTORIZE:
            ctx_msgs = ContextMemoryManager._handle_strategy_vectorize_history(
                chat_history,
                max_context_msgs
            )

        else:
            ctx_msgs = ContextMemoryManager._handle_strategy_forget_oldest(
                chat_history,
                max_context_msgs
            )

        logger.info(f"[ChatContextManager.handle_context_leanmod] Handled the context for LeanMod.")

        return ctx_msgs

    @staticmethod
    def handle_context_voidforger(
        chat_history,
        voidforger: VoidForger
    ):
        ctx_msgs = ContextMemoryManager._handle_strategy_forget_oldest(
            chat_history, voidforger.short_term_memory_max_messages
        )

        logger.info(f"[ChatContextManager.handle_context_voidforger] Handled the context for VoidForger.")

        return ctx_msgs

    @staticmethod
    def _handle_strategy_vectorize_history(
        chat_history,
        max_messages
    ):
        try:
            ctx_msgs = ContextMemoryManager.store_context_memory_as_embedding(
                message_history=chat_history,
                maximum_allowed_messages=max_messages
            )

            logger.info(
                f"[ChatContextManager._handle_strategy_vectorize_history] Vectorized the history, returning trimmed messages.")

        except Exception as e:
            logger.error(
                f"[ChatContextManager._handle_strategy_vectorize_history] Error in vectorization of the message history: {e}")

            ctx_msgs = chat_history

        return ctx_msgs

    @staticmethod
    def _handle_strategy_stop_conversation(
        chat_history,
        max_messages
    ):

        try:
            ctx_msgs = ContextMemoryManager.stop_communication_at_threshold(
                chat_history,
                max_messages
            )

            logger.info(f"[ChatContextManager._handle_strategy_stop_conversation] Stopped the conversation.")

        except Exception as e:
            ctx_msgs = chat_history

            logger.error(
                f"[ChatContextManager._handle_strategy_stop_conversation] Error stopping the conversation: {e}")

        return ctx_msgs

    @staticmethod
    def _handle_strategy_forget_oldest(
        chat_history,
        max_messages
    ):
        try:
            ctx_msgs = ContextMemoryManager.forget_oldest_chat_messages(
                chat_history,
                max_messages
            )

            logger.info(f"[ChatContextManager._handle_strategy_forget_oldest] Forgot the oldest messages.")

        except Exception as e:
            ctx_msgs = chat_history

            logger.error(
                f"[ChatContextManager._handle_strategy_forget_oldest] Error forgetting the oldest messages: {e}")

        return ctx_msgs

    @staticmethod
    def _generate_query_embedding(
        assistant: Assistant,
        query: str
    ) -> List[float]:

        from apps.core.generative_ai.gpt_openai_manager import (
            OpenAIGPTClientManager
        )

        c = OpenAIGPTClientManager.get_naked_client(
            llm_model=assistant.llm_model
        )

        response = c.embeddings.create(
            input=query,
            model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE
        )

        return response.data[0].embedding

    @staticmethod
    def _generate_query_embedding_leanmod(
        leanmod_assistant: LeanAssistant,
        query: str
    ) -> List[float]:

        from apps.core.generative_ai.gpt_openai_manager import (
            OpenAIGPTClientManager
        )

        c = OpenAIGPTClientManager.get_naked_client(
            llm_model=leanmod_assistant.llm_model
        )

        response = c.embeddings.create(
            input=query,
            model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE
        )

        return response.data[0].embedding

    @staticmethod
    def search_old_chat_messages(
        assistant_chat_id: int,
        query: str,
        n_results: int = ASSISTANT_DEFAULT_SEARCH_RESULTS_OLD_CHAT_MESSAGES
    ) -> List[Dict]:

        old_chat_messages_index_path = os.path.join(
            VECTOR_INDEX_PATH_ASSISTANT_CHAT_MESSAGES,
            f'assistant_chat_index_{assistant_chat_id}.index'
        )

        if os.path.exists(old_chat_messages_index_path):
            old_chat_messages_index = faiss.read_index(
                old_chat_messages_index_path
            )
        else:
            old_chat_messages_index = faiss.IndexIDMap(
                faiss.IndexFlatL2(
                    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
                )
            )

            faiss.write_index(
                old_chat_messages_index,
                old_chat_messages_index_path
            )

        try:
            chat_object = MultimodalChat.objects.get(
                id=assistant_chat_id
            )

            assistant_object = chat_object.assistant

        except Exception as e:
            print(f"Error getting the chat object: {e}")
            logger.error(f"Error getting the chat object: {e}")

            return []

        query_vector = np.array(
            [
                ContextMemoryManager._generate_query_embedding(
                    assistant=assistant_object,
                    query=query
                )
            ],
            dtype=np.float32
        )

        if old_chat_messages_index is None:
            raise ValueError("[search_old_chat_messages] FAISS index not initialized or loaded properly.")

        distances, ids = old_chat_messages_index.search(
            query_vector,
            n_results
        )

        results = []

        for item_id, distance in zip(ids[0], distances[0]):

            if item_id == -1:
                continue

            try:
                instance = AssistantOldChatMessagesVectorData.objects.get(
                    id=item_id
                )

                results.append(
                    {
                        "id": instance.id,
                        "data": instance.raw_data,
                        "distance": distance,
                    }
                )

            except AssistantOldChatMessagesVectorData.DoesNotExist:
                print(
                    f"Warning: AssistantOldChatMessagesVectorData Instance with ID {item_id} not found in the vector database.")
                logger.error(
                    f"AssistantOldChatMessagesVectorData Instance with ID {item_id} not found in the vector database.")

        return results

    @staticmethod
    def search_old_leanmod_chat_messages(
        leanmod_chat_id: int,
        query: str,
        n_results: int = LEANMOD_ASSISTANT_DEFAULT_SEARCH_RESULTS_OLD_CHAT_MESSAGES
    ) -> List[Dict]:

        old_chat_messages_index_path = os.path.join(
            VECTOR_INDEX_PATH_LEANMOD_CHAT_MESSAGES,
            f'leanmod_chat_index_{leanmod_chat_id}.index'
        )

        if os.path.exists(old_chat_messages_index_path):
            old_chat_messages_index = faiss.read_index(
                old_chat_messages_index_path
            )
        else:
            old_chat_messages_index = faiss.IndexIDMap(
                faiss.IndexFlatL2(
                    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
                )
            )

            faiss.write_index(
                old_chat_messages_index,
                old_chat_messages_index_path
            )

        try:
            chat_object: MultimodalLeanChat = MultimodalLeanChat.objects.get(
                id=leanmod_chat_id
            )

            assistant_object = chat_object.lean_assistant

        except Exception as e:
            print(f"Error getting the LeanMod chat object: {e}")
            logger.error(f"Error getting the LeanMod chat object: {e}")

            return []

        query_vector = np.array(
            [
                ContextMemoryManager._generate_query_embedding_leanmod(
                    leanmod_assistant=assistant_object,
                    query=query
                )
            ],
            dtype=np.float32
        )

        if old_chat_messages_index is None:
            raise ValueError("[search_old_chat_messages] FAISS index not initialized or loaded properly.")

        distances, ids = old_chat_messages_index.search(
            query_vector,
            n_results
        )

        results = []

        for item_id, distance in zip(ids[0], distances[0]):

            if item_id == -1:
                continue

            try:
                instance = LeanModOldChatMessagesVectorData.objects.get(
                    id=item_id
                )

                results.append(
                    {
                        "id": instance.id,
                        "data": instance.raw_data,
                        "distance": distance,
                    }
                )

            except LeanModOldChatMessagesVectorData.DoesNotExist:
                print(
                    f"Warning: LeanModOldChatMessagesVectorData Instance with ID {item_id} not found in the vector database.")
                logger.error(
                    f"LeanModOldChatMessagesVectorData Instance with ID {item_id} not found in the vector database.")

        return results
