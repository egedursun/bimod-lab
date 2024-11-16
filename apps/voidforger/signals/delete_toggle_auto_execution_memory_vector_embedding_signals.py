#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_toggle_auto_execution_memory_vector_embedding_signals.py
#  Last Modified: 2024-11-15 16:17:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 16:17:35
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

from apps.voidforger.models import VoidForgerToggleAutoExecutionLog, VoidForgerAutoExecutionMemoryVectorData

logger = logging.getLogger(__name__)


@receiver(pre_delete, sender=VoidForgerToggleAutoExecutionLog)
def remove_vector_from_index_on_auto_execution_memory_delete(sender, instance, **kwargs):
    try:
        vector_data_instance = VoidForgerAutoExecutionMemoryVectorData.objects.get(
            voidforger_auto_execution_memory=instance)
        index_path = vector_data_instance._get_index_path()
        if os.path.exists(index_path):
            index = faiss.read_index(index_path)
            xids = np.array([vector_data_instance.id], dtype=np.int64)
            index.remove_ids(xids)
            faiss.write_index(index, index_path)
            logger.info(f"Removed vector data for VoidForgerToggleAutoExecutionLog with ID {instance.id} from index.")
            print(f"Removed vector data for VoidForgerToggleAutoExecutionLog with ID {instance.id} from index.")
        else:
            print(f"Index path {index_path} does not exist.")

        vector_data_instance.delete()
    except VoidForgerAutoExecutionMemoryVectorData.DoesNotExist:
        print(
            f"No VoidForgerAutoExecutionMemoryVectorData found for VoidForgerToggleAutoExecutionLog with ID {instance.id}.")
