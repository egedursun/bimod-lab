#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: assistant_context_history_vector_models.py
#  Last Modified: 2024-11-17 18:53:11
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-17 18:53:11
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import hashlib
import json
import logging
import os

import faiss
import numpy as np
from django.db import models

from apps.assistants.utils import VECTOR_INDEX_PATH_ASSISTANT_CHAT_MESSAGES, ContextManagementStrategyNames
from apps.core.semantor.utils import OpenAIEmbeddingModels, OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS

logger = logging.getLogger(__name__)


class AssistantOldChatMessagesVectorData(models.Model):
    assistant_chat_message = models.ForeignKey(
        'multimodal_chat.MultimodalChatMessage',
        on_delete=models.CASCADE,
        related_name='assistant_chat_message_vector_data'
    )

    raw_data = models.JSONField(
        blank=True,
        null=True
    )
    raw_data_hash = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    vector_data = models.JSONField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return str(self.assistant_chat_message.multimodal_chat.assistant.id) + " - " + str(
            self.assistant_chat_message.multimodal_chat.id) + " - " + str(
            self.assistant_chat_message.id) + " - " + self.created_at.strftime(
            "%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = "Assistant Old Chat Messages Vector Data"
        verbose_name_plural = "Assistant Old Chat Messages Vector Datas"
        indexes = [
            models.Index(fields=['assistant_chat_message']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

    def _get_index_path(self):
        assistant_chat_id = self.assistant_chat_message.multimodal_chat.id
        return os.path.join(
            VECTOR_INDEX_PATH_ASSISTANT_CHAT_MESSAGES,
            f'assistant_chat_index_{assistant_chat_id}.index'
        )

    def save(self, *args, **kwargs):

        if self.assistant_chat_message.multimodal_chat.assistant.context_overflow_strategy == ContextManagementStrategyNames.VECTORIZE:
            # Vectorize the messages if it is within the context management strategy of the Assistant object

            raw_data = {
                "assistant_id": self.assistant_chat_message.multimodal_chat.assistant.id,
                "chat_id": self.assistant_chat_message.multimodal_chat.id,
                "chat_message_id": self.assistant_chat_message.id,
                "sender_type": self.assistant_chat_message.sender_type,
                "message_text_content": self.assistant_chat_message.message_text_content,
                "message_image_contents": self.assistant_chat_message.message_image_contents,
                "message_file_contents": self.assistant_chat_message.message_file_contents,
                "message_audio": self.assistant_chat_message.message_audio,
                "sent_at": self.assistant_chat_message.sent_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            self.raw_data = raw_data

            ##############################
            # Convert to Vector
            ##############################

            self._generate_embedding(raw_data)

            ##############################
            # Save the Index to Vector DB
            ##############################

            if self.has_raw_data_changed() or self.vector_data is None or self.vector_data == []:
                print("Vector data has changed, generating new embedding...")
                self._generate_embedding(raw_data)
            else:
                print("Vector data has not changed, using existing embedding...")
                pass

            super().save(*args, **kwargs)

            self._save_embedding()

        else:
            super().save(*args, **kwargs)

    def _generate_embedding(self, raw_data):
        from apps.core.generative_ai.gpt_openai_manager import OpenAIGPTClientManager
        c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.assistant_chat_message.multimodal_chat.assistant.llm_model
        )
        raw_data_text = json.dumps(raw_data, indent=2)
        try:
            response = c.embeddings.create(
                input=raw_data_text,
                model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE
            )
            embedding_vector = response.data[0].embedding
            self.vector_data = embedding_vector
        except Exception as e:
            logger.error(f"Error in generating embedding: {e}")
            self.vector_data = []

    def _save_embedding(self):
        if self.vector_data:
            x = np.array([self.vector_data], dtype=np.float32).reshape(
                1,
                OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
            )
            xids = np.array([self.id], dtype=np.int64)
            index_path = self._get_index_path()
            if not os.path.exists(index_path):
                index = faiss.IndexIDMap(faiss.IndexFlatL2(OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS))
            else:
                index = faiss.read_index(index_path)
                if not isinstance(index, faiss.IndexIDMap):
                    index = faiss.IndexIDMap(index)
                index.remove_ids(xids)

            index.add_with_ids(x, xids)
            faiss.write_index(index, index_path)

    def has_raw_data_changed(self):
        raw_data_str = json.dumps(self.raw_data, sort_keys=True)
        new_raw_data_hash = hashlib.sha256(raw_data_str.encode('utf-8')).hexdigest()
        if self.raw_data_hash == new_raw_data_hash:
            return False
        self.raw_data_hash = new_raw_data_hash
        return True
