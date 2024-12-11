#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sql_database_vector_models.py
#  Last Modified: 2024-12-03 22:29:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-03 22:29:18
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

from django.db import models

from apps.datasource_sql.utils import (
    VECTOR_INDEX_PATH_SQL_SCHEMAS,
)

logger = logging.getLogger(__name__)


class SQLSchemaChunkVectorData(models.Model):
    sql_database = models.ForeignKey(
        'datasource_sql.SQLDatabaseConnection',
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
        return self.sql_database.database_name + " - " + self.sql_database.name + " - " + str(self.sql_database.host)

    class Meta:
        verbose_name = "SQL Schema Chunk Vector Data"
        verbose_name_plural = "SQL Schema Chunk Vector Data"

        indexes = [
            models.Index(fields=[
                'sql_database'
            ]),
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'updated_at'
            ]),
        ]

    def _get_index_path(self):
        storage_id = self.sql_database.id

        return os.path.join(
            VECTOR_INDEX_PATH_SQL_SCHEMAS,
            f'sql_schemas_index_{storage_id}.index'
        )
