#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: refresh_sql_schema_views.py
#  Last Modified: 2024-12-04 21:09:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-04 21:09:48
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

from apps.datasource_sql.models import (
    SQLDatabaseConnection,
    SQLSchemaChunkVectorData
)
from apps.datasource_sql.tasks import (
    handle_embedding_task
)

from apps.datasource_sql.utils import (
    SQL_SCHEMA_VECTOR_CHUNK_SIZE,
    SQL_SCHEMA_VECTOR_CHUNK_OVERLAP,
    VECTOR_INDEX_PATH_SQL_SCHEMAS
)

logger = logging.getLogger(__name__)


class SQLDatabaseView_ManagerRefreshSchema(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        connection_id = kwargs.get('pk')

        sql_database = SQLDatabaseConnection.objects.get(
            id=connection_id
        )

        if not sql_database:
            messages.error(request, 'SQL Database Connection is not found, unexpected error.')

        try:

            # re-save the SQL db to refresh the schema
            sql_database.save()

            ################################################################################################
            # Clean the old chunks (if exists)
            ################################################################################################

            vector_data_instances = SQLSchemaChunkVectorData.objects.filter(
                sql_database=sql_database
            ).all()

            storage_id = sql_database.id

            index_path = os.path.join(
                VECTOR_INDEX_PATH_SQL_SCHEMAS,
                f'sql_schemas_index_{storage_id}.index'
            )

            # Clean the vector index items
            if os.path.exists(index_path):
                index = faiss.read_index(index_path)

                xids = np.array(
                    [
                        vector_data_instance.id for vector_data_instance in vector_data_instances
                    ]
                )

                index.remove_ids(xids)

                faiss.write_index(index, index_path)

                logger.info(f"Removed vector data for [SQL] with ID {sql_database.id} from index.")

            else:
                logger.warning(f"Index file not found for SQLDatabaseConnection with ID {sql_database.id}.")

            for vector_data_instance in vector_data_instances:
                vector_data_instance.delete()

            ################################################################################################
            # / Clean the old chunks (if exists)
            ################################################################################################

            # ...

            ################################################################################################
            # Re-Run Embedding Process
            ################################################################################################

            schema = sql_database.schema_data_json

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
                    sql_database=sql_database,
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

            logger.info(f"Successfully updated the vector embeddings for SQLDatabaseConnection.")

            ################################################################################################
            # / Re-Run Embedding Process
            ################################################################################################

            messages.success(request, 'SQL Schema Refreshed Successfully.')
            logger.info(f"SQL Schema Refreshed Successfully.")

        except Exception as e:
            messages.error(request, f'Error refreshing SQL Schema: {e}')

            logger.error(f"Error refreshing SQL Schema: {e}")

        return redirect('datasource_sql:list')
