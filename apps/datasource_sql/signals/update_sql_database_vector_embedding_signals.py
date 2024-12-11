#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_sql_database_vector_embedding_signals.py
#  Last Modified: 2024-12-03 21:38:20
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-03 22:50:55
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import json
import logging

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.datasource_sql.models import (
    SQLDatabaseConnection,
    SQLSchemaChunkVectorData,
)
from apps.datasource_sql.tasks import (
    handle_embedding_task
)

from apps.datasource_sql.utils import (
    SQL_SCHEMA_VECTOR_CHUNK_OVERLAP,
    SQL_SCHEMA_VECTOR_CHUNK_SIZE
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=SQLDatabaseConnection)
def update_sql_database_vector_embedding_after_save(
    sender,
    instance,
    created,
    **kwargs
):
    if created:

        try:
            instance: SQLDatabaseConnection
            schema = instance.schema_data_json

            json_text = json.dumps(
                schema,
                indent=2
            )

            splitter = RecursiveCharacterTextSplitter(
                json_text,
                chunk_size=SQL_SCHEMA_VECTOR_CHUNK_SIZE,
                chunk_overlap=SQL_SCHEMA_VECTOR_CHUNK_OVERLAP
            )

            chunks = splitter.split_text(json_text)

            for i, chunk in enumerate(chunks):
                chunk_vector_data = SQLSchemaChunkVectorData.objects.create(
                    sql_database=instance,
                    raw_data=chunk,
                )

                ##############################
                # Save the Index to Vector DB
                ##############################

                handle_embedding_task(
                    vector_id=chunk_vector_data.id,
                    raw_data=chunk_vector_data.raw_data,
                )

                ##############################

            logger.info(f"Successfully updated the vector embeddings for SQLDatabaseConnection with ID {instance.id}.")

        except Exception as e:
            logger.error(f"Error in post-save embedding update: {e}")

    else:
        logger.info(f"SQLDatabaseConnection with ID {instance.id} vectorization has already been created, skipping.")
        pass
