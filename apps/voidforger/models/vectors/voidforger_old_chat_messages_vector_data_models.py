#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_old_chat_messages_vector_data_models.py
#  Last Modified: 2024-11-15 16:08:02
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 17:23:34
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

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from apps.voidforger.utils import (
    VECTOR_INDEX_PATH_CHAT_MESSAGES,
    OpenAIEmbeddingModels,
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
)

logger = logging.getLogger(__name__)


class VoidForgerOldChatMessagesVectorData(models.Model):
    voidforger_chat_message = models.ForeignKey(
        'voidforger.MultimodalVoidForgerChatMessage',
        on_delete=models.CASCADE,
        related_name='voidforger_chat_message_vector_data'
    )

    raw_data = models.JSONField(blank=True, null=True)

    raw_data_hash = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    vector_data = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.voidforger_chat_message.multimodal_voidforger_chat.voidforger.id) + " - " + str(
            self.voidforger_chat_message.multimodal_voidforger_chat.id) + " - " + str(
            self.voidforger_chat_message.id) + " - " + self.created_at.strftime(
            "%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = "VoidForger Old Chat Messages Vector Data"
        verbose_name_plural = "VoidForger Old Chat Messages Vector Datas"

        indexes = [
            models.Index(fields=[
                'voidforger_chat_message'
            ]),
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'updated_at'
            ]),
        ]

    def _get_index_path(self):
        voidforger_chat_id = self.voidforger_chat_message.multimodal_voidforger_chat.id

        return os.path.join(
            VECTOR_INDEX_PATH_CHAT_MESSAGES,
            f'voidforger_chat_index_{voidforger_chat_id}.index'
        )

    def save(self, *args, **kwargs):

        vectorization_text = (
            self.voidforger_chat_message.message_text_content
        )

        splitter = RecursiveCharacterTextSplitter(
            vectorization_text,
            chunk_size=3_000,
            chunk_overlap=0
        )

        chunks = splitter.split_text(vectorization_text)

        if len(chunks) > 2:
            vectorization_text = chunks[0] + " ... " + chunks[-1]

        else:
            vectorization_text = " ".join(chunks) if chunks else ""

        raw_data = {
            "voidforger_id": self.voidforger_chat_message.multimodal_voidforger_chat.voidforger.id,
            "chat_id": self.voidforger_chat_message.multimodal_voidforger_chat.id,
            "chat_message_id": self.voidforger_chat_message.id,
            "sender_type": self.voidforger_chat_message.sender_type,
            "message_text_content": vectorization_text,
            "message_image_contents": self.voidforger_chat_message.message_image_contents,
            "message_file_contents": self.voidforger_chat_message.message_file_contents,
            "message_audio": self.voidforger_chat_message.message_audio,
            "sent_at": self.voidforger_chat_message.sent_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.raw_data = raw_data

        ##############################
        # Convert to Vector
        ##############################

        self._generate_embedding(raw_data)

        ##############################
        # Save the Index to Vector DB
        ##############################

        if (
            self.has_raw_data_changed() or
            self.vector_data is None or
            self.vector_data == []
        ):
            self._generate_embedding(raw_data)

        else:
            pass

        super().save(*args, **kwargs)

        self._save_embedding()

    def _generate_embedding(self, raw_data):
        from apps.core.generative_ai.gpt_openai_manager import (
            OpenAIGPTClientManager
        )

        c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.voidforger_chat_message.multimodal_voidforger_chat.voidforger.llm_model
        )

        raw_data_text = json.dumps(
            raw_data,
            indent=2
        )

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
            x = np.array(
                [self.vector_data],
                dtype=np.float32
            ).reshape(
                1,
                OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
            )

            xids = np.array(
                [
                    self.id
                ],
                dtype=np.int64
            )

            index_path = self._get_index_path()

            if not os.path.exists(index_path):

                index = faiss.IndexIDMap(
                    faiss.IndexFlatL2(
                        OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
                    )
                )

            else:
                index = faiss.read_index(index_path)

                if not isinstance(
                    index,
                    faiss.IndexIDMap
                ):
                    index = faiss.IndexIDMap(index)

                index.remove_ids(xids)

            index.add_with_ids(
                x,
                xids
            )

            faiss.write_index(
                index,
                index_path
            )

    def has_raw_data_changed(self):
        raw_data_str = json.dumps(
            self.raw_data,
            sort_keys=True
        )

        new_raw_data_hash = hashlib.sha256(
            raw_data_str.encode('utf-8')
        ).hexdigest()

        if self.raw_data_hash == new_raw_data_hash:
            return False

        self.raw_data_hash = new_raw_data_hash
        return True
