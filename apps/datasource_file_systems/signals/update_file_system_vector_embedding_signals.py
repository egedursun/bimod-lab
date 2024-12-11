#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_file_system_vector_embedding_signals.py
#  Last Modified: 2024-12-03 23:46:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-04 00:34:05
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

from django.db.models.signals import (
    post_save
)

from django.dispatch import receiver

from apps.core.file_systems.file_systems_executor import (
    FileSystemsExecutor
)

from apps.datasource_file_systems.models import (
    DataSourceFileSystem,
    FileSystemDirectorySchemaChunkVectorData,
)

from apps.datasource_file_systems.tasks import (
    handle_embedding_task
)

from apps.datasource_file_systems.utils import (
    FILE_SYSTEM_DIRECTORY_SCHEMA_VECTOR_CHUNK_OVERLAP,
    FILE_SYSTEM_DIRECTORY_SCHEMA_VECTOR_CHUNK_SIZE
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=DataSourceFileSystem)
def update_file_system_vector_embedding_after_save(
    sender,
    instance,
    created,
    **kwargs
):
    if created:

        try:
            instance: DataSourceFileSystem

            schema = FileSystemsExecutor(instance).schema_str
            instance.file_directory_tree = schema

            instance.save()

            json_text = json.dumps(schema, indent=2)

            splitter = RecursiveCharacterTextSplitter(
                json_text,
                chunk_size=FILE_SYSTEM_DIRECTORY_SCHEMA_VECTOR_CHUNK_SIZE,
                chunk_overlap=FILE_SYSTEM_DIRECTORY_SCHEMA_VECTOR_CHUNK_OVERLAP
            )

            chunks = splitter.split_text(json_text)

            for i, chunk in enumerate(chunks):
                chunk_vector_data = FileSystemDirectorySchemaChunkVectorData.objects.create(
                    file_system=instance,
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

        except Exception as e:
            logger.error(f"Error in post-save embedding update: {e}")

    else:
        logger.info(f"File System with ID {instance.id} already exists, skipping vector embedding update.")
        pass
