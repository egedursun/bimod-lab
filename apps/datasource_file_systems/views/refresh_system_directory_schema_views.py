#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: refresh_system_directory_schema_views.py
#  Last Modified: 2024-12-04 21:41:55
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-04 21:41:55
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
import os

import faiss
import numpy as np
from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views import View

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from apps.core.file_systems.file_systems_executor import (
    FileSystemsExecutor
)

from apps.datasource_file_systems.models import (
    DataSourceFileSystem,
    FileSystemDirectorySchemaChunkVectorData
)

from apps.datasource_file_systems.tasks import (
    handle_embedding_task
)

from apps.datasource_file_systems.utils import (
    VECTOR_INDEX_PATH_FILE_SYSTEM_DIRECTORY_SCHEMAS,
    FILE_SYSTEM_DIRECTORY_SCHEMA_VECTOR_CHUNK_SIZE,
    FILE_SYSTEM_DIRECTORY_SCHEMA_VECTOR_CHUNK_OVERLAP
)

logger = logging.getLogger(__name__)


class FileSystemView_RefreshSchema(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        connection_id = kwargs.get('pk')

        file_system = DataSourceFileSystem.objects.get(id=connection_id)
        if not file_system:
            messages.error(request, 'File System Connection is not found, unexpected error.')

        try:

            # explicitly re-define the file directory tree schema for file system
            schema = FileSystemsExecutor(file_system).schema_str
            file_system.file_directory_tree = schema
            file_system.save()

            ################################################################################################
            # Clean the old chunks (if exists)
            ################################################################################################

            vector_data_instances = FileSystemDirectorySchemaChunkVectorData.objects.filter(
                file_system=file_system
            ).all()

            storage_id = file_system.id
            index_path = os.path.join(
                VECTOR_INDEX_PATH_FILE_SYSTEM_DIRECTORY_SCHEMAS,
                f'file_system_directory_schemas_index_{storage_id}.index'
            )

            # Clean the vector index items
            if os.path.exists(index_path):
                index = faiss.read_index(index_path)

                xids = np.array([
                    vector_data_instance.id for vector_data_instance in vector_data_instances
                ])

                index.remove_ids(xids)

                faiss.write_index(index, index_path)

                logger.info(f"Removed vector data for [SSH File System] with ID {file_system.id} from index.")

            else:
                print(f"Index path {index_path} does not exist, skipping deletion of index items...")

            # Clean the ORM object
            for vector_data_instance in vector_data_instances:
                vector_data_instance.delete()

            ################################################################################################
            # / Clean the old chunks (if exists)
            ################################################################################################

            # ...

            ################################################################################################
            # Re-Run Embedding Process
            ################################################################################################

            schema = file_system.file_directory_tree

            json_text = json.dumps(schema, indent=2)

            splitter = RecursiveCharacterTextSplitter(
                json_text,
                chunk_size=FILE_SYSTEM_DIRECTORY_SCHEMA_VECTOR_CHUNK_SIZE,
                chunk_overlap=FILE_SYSTEM_DIRECTORY_SCHEMA_VECTOR_CHUNK_OVERLAP
            )

            chunks = splitter.split_text(json_text)

            for i, chunk in enumerate(chunks):
                chunk_vector_data = FileSystemDirectorySchemaChunkVectorData.objects.create(
                    file_system=file_system,
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

            logger.info(f"Successfully updated the vector embeddings for DataSourceFileSystem.")
            print("All chunks have been embedded successfully.")

            ################################################################################################
            # / Re-Run Embedding Process
            ################################################################################################

            messages.success(request, 'File System Directory Schema Refreshed Successfully.')
            logger.info(f"File System Directory Schema Refreshed Successfully.")

        except Exception as e:
            messages.error(request, f'Error refreshing File System Directory Schema: {e}')
            logger.error(f"Error refreshing File System Directory Schema: {e}")

        return redirect('datasource_file_systems:list')
