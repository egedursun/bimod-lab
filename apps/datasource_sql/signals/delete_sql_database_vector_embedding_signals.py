#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_sql_database_vector_embedding_signals.py
#  Last Modified: 2024-12-03 21:38:20
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-03 22:50:51
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

import faiss
import numpy as np
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from apps.datasource_sql.models import (
    SQLDatabaseConnection,
    SQLSchemaChunkVectorData,
)
from apps.datasource_sql.utils import VECTOR_INDEX_PATH_SQL_SCHEMAS

logger = logging.getLogger(__name__)


@receiver(pre_delete, sender=SQLDatabaseConnection)
def remove_vector_from_index_on_sql_database_delete(sender, instance, **kwargs):
    try:
        vector_data_instances = SQLSchemaChunkVectorData.objects.filter(
            sql_database=instance
        ).all()

        if not vector_data_instances:
            print(f"No vector data found for SQLDatabaseConnection with ID {instance.id}.")
            return

        storage_id = instance.id
        index_path = os.path.join(
            VECTOR_INDEX_PATH_SQL_SCHEMAS,
            f'sql_schemas_index_{storage_id}.index'
        )

        if os.path.exists(index_path):
            index = faiss.read_index(index_path)

            xids = np.array([
                vector_data_instance.id for vector_data_instance in vector_data_instances
            ])

            index.remove_ids(xids)

            faiss.write_index(index, index_path)

            logger.info(f"Removed vector data for SQLDatabaseConnection with ID {instance.id} from index.")
            print(f"Removed vector data for SQLDatabaseConnection with ID {instance.id} from index.")

        else:
            print(f"Index path {index_path} does not exist.")

        for vector_data_instance in vector_data_instances:
            vector_data_instance.delete()

    except SQLSchemaChunkVectorData.DoesNotExist:
        print(
            f"No SQLSchemaChunkVectorData found for SQLDatabaseConnection with ID {instance.id}.")
