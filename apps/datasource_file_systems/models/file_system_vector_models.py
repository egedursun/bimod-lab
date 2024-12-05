#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: file_system_vector_models.py
#  Last Modified: 2024-12-04 00:23:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-04 00:23:04
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

from apps.datasource_file_systems.tasks import handle_embedding_task
from apps.datasource_file_systems.utils import (
    VECTOR_INDEX_PATH_FILE_SYSTEM_DIRECTORY_SCHEMAS
)

logger = logging.getLogger(__name__)


class FileSystemDirectorySchemaChunkVectorData(models.Model):
    file_system = models.ForeignKey(
        'datasource_file_systems.DataSourceFileSystem',
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
        return self.file_system.name + " - " + str(self.file_system.host_url)

    class Meta:
        verbose_name = "File System Directory Schema Chunk Vector Data"
        verbose_name_plural = "File System Directory Schema Chunk Vector Data"
        indexes = [
            models.Index(fields=[
                'file_system'
            ]),
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'updated_at'
            ]),
        ]

    def get_index_path(self):
        storage_id = self.file_system.id
        return os.path.join(
            VECTOR_INDEX_PATH_FILE_SYSTEM_DIRECTORY_SCHEMAS,
            f'file_system_directory_schemas_index_{storage_id}.index'
        )
