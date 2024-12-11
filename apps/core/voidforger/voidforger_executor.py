#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_executor.py
#  Last Modified: 2024-11-15 18:43:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 18:43:16
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
import uuid

from typing import (
    List,
    Dict
)

import faiss
import numpy as np

from django.contrib.auth.models import (
    User
)

from django.utils import timezone

from apps.core.generative_ai.generative_ai_decode_manager import (
    GenerativeAIDecodeController
)

from apps.core.generative_ai.gpt_openai_manager import (
    OpenAIGPTClientManager
)

from apps.core.tool_calls.utils import (
    VoidForgerModesNames
)

from apps.core.voidforger.utils import (
    VOIDFORGER_DEFAULT_SEARCH_RESULTS_OLD_CHAT_MESSAGES,
    VOIDFORGER_DEFAULT_SEARCH_RESULTS_ACTION_HISTORY_LOGS,
    VOIDFORGER_DEFAULT_SEARCH_RESULTS_AUTO_EXECUTION_LOGS
)

from apps.multimodal_chat.utils import (
    generate_chat_name,
    SourcesForMultimodalChatsNames
)

from apps.voidforger.models import (
    VoidForger,
    VoidForgerActionMemoryVectorData,
    VoidForgerOldChatMessagesVectorData,
    VoidForgerAutoExecutionMemoryVectorData,
    MultimodalVoidForgerChatMessage,
    MultimodalVoidForgerChat,
    VoidForgerToggleAutoExecutionLog,
    VoidForgerActionMemoryLog
)

from apps.voidforger.utils import (
    OpenAIEmbeddingModels,
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS,
    VECTOR_INDEX_PATH_ACTION_MEMORIES,
    VECTOR_INDEX_PATH_CHAT_MESSAGES,
    VECTOR_INDEX_PATH_AUTO_EXECUTION_MEMORIES,
    VoidForgerRuntimeStatusesNames,
    VoidForgerToggleAutoExecutionActionTypesNames,
    VoidForgerActionTypesNames
)

logger = logging.getLogger(__name__)


class VoidForgerExecutionManager:

    def __init__(
        self,
        user: User,
        voidforger_id: int,
        vector_dim: int = OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
    ):
        self.voidforger_id = voidforger_id

        self.voidforger = VoidForger.objects.get(
            id=voidforger_id
        )

        self.llm_model = self.voidforger.llm_model
        self.vector_dim = vector_dim

        self.action_memory_logs_index_path = os.path.join(
            VECTOR_INDEX_PATH_ACTION_MEMORIES,
            f'voidforger_index_{self.voidforger_id}.index'
        )

        self.auto_execution_logs_index_path = os.path.join(
            VECTOR_INDEX_PATH_AUTO_EXECUTION_MEMORIES,
            f'voidforger_index_{self.voidforger_id}.index'
        )

        if os.path.exists(
            self.action_memory_logs_index_path
        ):

            self.action_memory_logs_index = faiss.read_index(
                self.action_memory_logs_index_path
            )

        else:

            self.action_memory_logs_index = faiss.IndexIDMap(
                faiss.IndexFlatL2(
                    self.vector_dim
                )
            )

            faiss.write_index(
                self.action_memory_logs_index,
                self.action_memory_logs_index_path
            )

        if os.path.exists(
            self.auto_execution_logs_index_path
        ):

            self.auto_execution_logs_index = faiss.read_index(
                self.auto_execution_logs_index_path
            )

        else:

            self.auto_execution_logs_index = faiss.IndexIDMap(
                faiss.IndexFlatL2(
                    self.vector_dim
                )
            )

            faiss.write_index(
                self.auto_execution_logs_index,
                self.auto_execution_logs_index_path
            )

    def _generate_query_embedding(
        self,
        query: str
    ) -> List[float]:

        c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.llm_model
        )

        response = c.embeddings.create(
            input=query,
            model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE
        )

        return response.data[0].embedding

    def run_cycle(
        self,
        trigger
    ):

        # If paused, do not run.

        if self.voidforger.runtime_status == VoidForgerRuntimeStatusesNames.PAUSED:
            error = "VoidForger is paused, cannot run."
            logger.error(error)

            return error

        # Convert to running state.
        self.voidforger.runtime_status = VoidForgerRuntimeStatusesNames.WORKING
        self.voidforger.last_auto_execution_started_at = timezone.now()

        self.voidforger.save()

        try:
            chat = MultimodalVoidForgerChat.objects.create(
                voidforger=self.voidforger,
                user=self.voidforger.user,
                chat_name=generate_chat_name() + str(uuid.uuid4()),
                created_by_user=self.voidforger.llm_model.created_by_user,
                chat_source=SourcesForMultimodalChatsNames.ORCHESTRATION
            )

            for current_action_index in range(
                self.voidforger.maximum_actions_per_cycle
            ):

                try:
                    user_message = MultimodalVoidForgerChatMessage.objects.create(
                        multimodal_voidforger_chat=chat,
                        sender_type='USER',
                        message_text_content=f"""

                            ================================================================================================
                            EXECUTION CYCLE CALL
                                - **ATTENTION:** This is 'NOT' chat mode.
                            ================================================================================================
                                - Trigger Source: {trigger}
                                - (If trigger is {VoidForgerModesNames.AUTOMATED}, this is an automated execution cycle call.)
                                - (If trigger is {VoidForgerModesNames.MANUAL}, this is a manual execution cycle call triggered by the user.)
                                - In both of these cases, user is not there to respond to you, this is not a chat session.
                                - You are expected to perform your duties as a VoidForger meta-orchestrator.
                            ================================================================================================

                            - [1] Execution Cycle No: {self.voidforger.auto_run_current_cycle}
                                - [1.1] Maximum Lifetime Cycles: {self.voidforger.auto_run_max_lifetime_cycles}

                            - [2] Total Number of Actions Allowed: {self.voidforger.maximum_actions_per_cycle}
                                - [2.1] Your **CURRENT ACTION INDEX**: {current_action_index} out of {self.voidforger.maximum_actions_per_cycle}

                            ================================================================================================
                        """,
                        message_image_contents=[],
                        message_file_contents=[]
                    )

                    internal_llm_client_voidforger = GenerativeAIDecodeController.get_voidforger(
                        user=self.voidforger.user,
                        assistant=chat.voidforger,
                        multimodal_chat=chat
                    )

                    response = internal_llm_client_voidforger.respond(
                        latest_message=user_message,
                        current_mode=VoidForgerModesNames.CHAT,
                        image_uris=[], file_uris=[]
                    )

                    assistant_message = MultimodalVoidForgerChatMessage.objects.create(
                        multimodal_voidforger_chat=chat,
                        sender_type='ASSISTANT',
                        message_text_content=response
                    )

                    VoidForgerActionMemoryLog.objects.create(
                        voidforger=self.voidforger,
                        action_type=VoidForgerActionTypesNames.NATURAL_LANGUAGE_RESPONSE,
                        action_order_raw_text=response
                    )

                except Exception as e:
                    error = f"Error while processing execution cycle: " + str(e)
                    logger.error(error)
                    continue

        except Exception as e:
            error = f"Error while processing execution cycle(s): " + str(e)
            logger.error(error)

            self.voidforger.runtime_status = VoidForgerRuntimeStatusesNames.ACTIVE
            self.voidforger.last_auto_execution_ended_at = timezone.now()

            self.voidforger.save()

            return error

        # Convert to active state.
        self.voidforger.runtime_status = VoidForgerRuntimeStatusesNames.ACTIVE
        self.voidforger.last_auto_execution_ended_at = timezone.now()

        self.voidforger.save()

        # Check the runtime cycle, and stop if it exceeds the maximum lifetime cycles.
        self.voidforger.auto_run_current_cycle += 1

        self.voidforger.save()

        if self.voidforger.auto_run_current_cycle >= self.voidforger.auto_run_max_lifetime_cycles:
            self.voidforger.auto_run_current_cycle = 0
            self.voidforger.runtime_status = VoidForgerRuntimeStatusesNames.PAUSED
            self.voidforger.last_auto_execution_started_at = None
            self.voidforger.last_auto_execution_ended_at = None

            self.voidforger.save()

            VoidForgerToggleAutoExecutionLog.objects.create(
                voidforger=self.voidforger,
                action_type=VoidForgerToggleAutoExecutionActionTypesNames.END_OF_LIFE,
                responsible_user=self.voidforger.user
            )

            info_msg = "Auto Execution has ended due to reaching the maximum cycle count."

            logger.info(info_msg)

        return None

    def search_old_chat_messages(
        self,
        voidforger_chat_id: int,
        query: str,
        n_results: int = VOIDFORGER_DEFAULT_SEARCH_RESULTS_OLD_CHAT_MESSAGES
    ) -> List[Dict]:
        old_chat_messages_index_path = os.path.join(
            VECTOR_INDEX_PATH_CHAT_MESSAGES,
            f'voidforger_chat_index_{voidforger_chat_id}.index'
        )

        if os.path.exists(old_chat_messages_index_path):
            old_chat_messages_index = faiss.read_index(
                old_chat_messages_index_path
            )

        else:
            old_chat_messages_index = faiss.IndexIDMap(
                faiss.IndexFlatL2(
                    self.vector_dim
                )
            )

            faiss.write_index(
                old_chat_messages_index,
                old_chat_messages_index_path
            )

        query_vector = np.array(
            [
                self._generate_query_embedding(query)
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
                instance = VoidForgerOldChatMessagesVectorData.objects.get(
                    id=item_id
                )

                results.append(
                    {
                        "id": instance.id,
                        "data": instance.raw_data,
                        "distance": distance,
                    }
                )

            except VoidForgerOldChatMessagesVectorData.DoesNotExist:
                logger.error(
                    f"VoidForgerOldChatMessagesVectorData Instance with ID {item_id} not found in the vector database.")

        return results

    def search_action_history_logs(
        self,
        query: str,
        n_results: int = VOIDFORGER_DEFAULT_SEARCH_RESULTS_ACTION_HISTORY_LOGS
    ) -> List[Dict]:

        query_vector = np.array(
            [
                self._generate_query_embedding(query)
            ],
            dtype=np.float32
        )

        if self.action_memory_logs_index is None:
            raise ValueError("[search_action_history_logs] FAISS index not initialized or loaded properly.")

        distances, ids = self.action_memory_logs_index.search(
            query_vector,
            n_results
        )

        results = []

        for item_id, distance in zip(
            ids[0],
            distances[0]
        ):

            if item_id == -1:
                continue

            try:
                instance = VoidForgerActionMemoryVectorData.objects.get(
                    id=item_id
                )

                results.append(
                    {
                        "id": instance.id,
                        "data": instance.raw_data,
                        "distance": distance,
                    }
                )

            except VoidForgerActionMemoryVectorData.DoesNotExist:
                logger.error(
                    f"VoidForgerActionMemoryVectorData Instance with ID {item_id} not found in the vector database.")

        return results

    def search_auto_execution_logs(
        self,
        query: str,
        n_results: int = VOIDFORGER_DEFAULT_SEARCH_RESULTS_AUTO_EXECUTION_LOGS
    ) -> List[Dict]:

        query_vector = np.array(
            [
                self._generate_query_embedding(query)
            ],
            dtype=np.float32
        )

        if self.auto_execution_logs_index is None:
            raise ValueError("[search_auto_execution_logs] FAISS index not initialized or loaded properly.")

        distances, ids = self.auto_execution_logs_index.search(
            query_vector,
            n_results
        )

        results = []

        for item_id, distance in zip(
            ids[0],
            distances[0]
        ):

            if item_id == -1:
                continue

            try:
                instance = VoidForgerAutoExecutionMemoryVectorData.objects.get(
                    id=item_id
                )

                results.append(
                    {
                        "id": instance.id,
                        "data": instance.raw_data,
                        "distance": distance,
                    }
                )

            except VoidForgerAutoExecutionMemoryVectorData.DoesNotExist:
                logger.error(
                    f"VoidForgerAutoExecutionMemoryVectorData Instance with ID {item_id} not found in the vector database.")

        return results
