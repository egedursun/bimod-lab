#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: refresh_nosql_schema_views.py
#  Last Modified: 2024-12-04 21:31:14
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-04 21:31:15
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from apps.datasource_nosql.models import (
    NoSQLDatabaseConnection,
    NoSQLSchemaChunkVectorData
)

from apps.datasource_nosql.tasks import (
    handle_embedding_task
)

from apps.datasource_nosql.utils import (
    VECTOR_INDEX_PATH_NOSQL_SCHEMAS,
    NOSQL_SCHEMA_VECTOR_CHUNK_SIZE,
    NOSQL_SCHEMA_VECTOR_CHUNK_OVERLAP
)

logger = logging.getLogger(__name__)


class NoSQLDatabaseView_ManagerRefreshSchema(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        connection_id = kwargs.get('pk')

        nosql_database = NoSQLDatabaseConnection.objects.get(id=connection_id)
        if not nosql_database:
            messages.error(request, 'NoSQL Database Connection is not found, unexpected error.')

        try:

            # re-save the NoSQL db to refresh the schema
            nosql_database.save()

            ################################################################################################
            # Clean the old chunks (if exists)
            ################################################################################################

            vector_data_instances = NoSQLSchemaChunkVectorData.objects.filter(
                nosql_database=nosql_database
            ).all()

            storage_id = nosql_database.id
            index_path = os.path.join(
                VECTOR_INDEX_PATH_NOSQL_SCHEMAS,
                f'nosql_schemas_index_{storage_id}.index'
            )

            # Clean the vector index items
            if os.path.exists(index_path):
                index = faiss.read_index(index_path)

                xids = np.array([
                    vector_data_instance.id for vector_data_instance in vector_data_instances
                ])

                index.remove_ids(xids)

                faiss.write_index(index, index_path)

                logger.info(f"Removed vector data for [NoSQL] with ID {nosql_database.id} from index.")

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

            schema = nosql_database.schema_data_json

            json_text = json.dumps(schema, indent=2)

            splitter = RecursiveCharacterTextSplitter(
                json_text,
                chunk_size=NOSQL_SCHEMA_VECTOR_CHUNK_SIZE,
                chunk_overlap=NOSQL_SCHEMA_VECTOR_CHUNK_OVERLAP
            )

            chunks = splitter.split_text(json_text)

            for i, chunk in enumerate(chunks):
                chunk_vector_data = NoSQLSchemaChunkVectorData.objects.create(
                    nosql_database=nosql_database,
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

            logger.info(f"Successfully updated the vector embeddings for NoSQLDatabaseConnection.")
            print("All chunks have been embedded successfully.")

            ################################################################################################
            # / Re-Run Embedding Process
            ################################################################################################

            messages.success(request, 'NoSQL Schema Refreshed Successfully.')
            logger.info(f"NoSQL Schema Refreshed Successfully.")

        except Exception as e:
            messages.error(request, f'Error refreshing NoSQL Schema: {e}')
            logger.error(f"Error refreshing NoSQL Schema: {e}")

        return redirect('datasource_nosql:list')
