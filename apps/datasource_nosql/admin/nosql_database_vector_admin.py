#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: nosql_database_vector_admin.py
#  Last Modified: 2024-12-03 23:23:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-03 23:23:05
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

"""
#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: nosql_database_vector_models.py
#  Last Modified: 2024-12-03 23:22:49
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-03 23:22:50
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

from apps.datasource_nosql.utils import VECTOR_INDEX_PATH_NOSQL_SCHEMAS, OpenAIEmbeddingModels, \
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS

logger = logging.getLogger(__name__)


class NoSQLSchemaChunkVectorData(models.Model):
    nosql_database = models.ForeignKey(
        'datasource_nosql.NoSQLDatabaseConnection',
        on_delete=models.CASCADE
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
        return self.nosql_database.bucket_name + " - " + self.nosql_database.name + " - " + str(
            self.nosql_database.host)

    class Meta:
        verbose_name = "NoSQL Schema Chunk Vector Data"
        verbose_name_plural = "NoSQL Schema Chunk Vector Data"
        indexes = [
            models.Index(fields=[
                'nosql_database'
            ]),
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'updated_at'
            ]),
        ]

    def _get_index_path(self):
        storage_id = self.nosql_database.id
        return os.path.join(VECTOR_INDEX_PATH_NOSQL_SCHEMAS, f'nosql_schemas_index_{storage_id}.index')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        ##############################
        # Save the Index to Vector DB
        ##############################

        self._generate_embedding(self.raw_data)
        self._save_embedding()

    def _generate_embedding(self, raw_data):
        from apps.core.generative_ai.gpt_openai_manager import (
            OpenAIGPTClientManager
        )

        c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.nosql_database.assistant.llm_model
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
            x = np.array(
                [self.vector_data],
                dtype=np.float32
            ).reshape(
                1,
                OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
            )

            xids = np.array([self.id], dtype=np.int64)
            index_path = self._get_index_path()

            if not os.path.exists(index_path):
                index = faiss.IndexIDMap(
                    faiss.IndexFlatL2(
                        OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
                    )
                )

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

"""

from django.contrib import admin

from apps.datasource_nosql.models import NoSQLSchemaChunkVectorData

from apps.datasource_nosql.utils import (
    NOSQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_LIST,
    NOSQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_FILTER,
    NOSQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_SEARCH
)


@admin.register(NoSQLSchemaChunkVectorData)
class NoSQLSchemaChunkVectorDataAdmin(admin.ModelAdmin):
    list_display = NOSQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_LIST
    list_filter = NOSQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_FILTER
    search_fields = NOSQL_SCHEMA_CHUNK_VECTOR_DATA_ADMIN_SEARCH

    ordering = ('created_at',)
