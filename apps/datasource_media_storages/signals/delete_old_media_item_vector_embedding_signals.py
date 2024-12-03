#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_old_media_item_vector_embedding_signals.py
#  Last Modified: 2024-12-01 23:31:56
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-02 00:27:28
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

from apps.datasource_media_storages.models import (
    DataSourceMediaStorageItem,
    MediaItemVectorData
)

logger = logging.getLogger(__name__)


@receiver(pre_delete, sender=DataSourceMediaStorageItem)
def remove_vector_from_index_on_media_item_delete(sender, instance, **kwargs):
    try:
        vector_data_instances = MediaItemVectorData.objects.filter(
            media_item=instance
        ).all()
        if not vector_data_instances:
            print(f"No vector data found for DataSourceMediaStorageItem with ID {instance.id}.")
            return

        index_path = vector_data_instances[0]._get_index_path()

        if os.path.exists(index_path):
            index = faiss.read_index(index_path)
            xids = np.array([vector_data_instance.id for vector_data_instance in vector_data_instances])
            index.remove_ids(xids)
            faiss.write_index(index, index_path)
            logger.info(f"Removed vector data for DataSourceMediaStorageItem with ID {instance.id} from index.")
            print(f"Removed vector data for DataSourceMediaStorageItem with ID {instance.id} from index.")

        else:
            print(f"Index path {index_path} does not exist.")

        for vector_data_instance in vector_data_instances:
            vector_data_instance.delete()

    except MediaItemVectorData.DoesNotExist:
        print(
            f"No MediaItemVectorData found for DataSourceMediaStorageItem with ID {instance.id}.")
