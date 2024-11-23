#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_old_chat_messages_vector_embedding_signals.py
#  Last Modified: 2024-11-15 16:17:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 18:18:33
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

from apps.voidforger.models import MultimodalVoidForgerChatMessage, VoidForgerOldChatMessagesVectorData

logger = logging.getLogger(__name__)


@receiver(pre_delete, sender=MultimodalVoidForgerChatMessage)
def remove_vector_from_index_on_voidforger_chat_message_delete(sender, instance, **kwargs):
    try:
        vector_data_instances = VoidForgerOldChatMessagesVectorData.objects.filter(
            voidforger_chat_message=instance
        ).all()

        if not vector_data_instances:
            print(f"No vector data found for MultimodalVoidForgerChatMessage with ID {instance.id}.")
            return

        index_path = vector_data_instances[0]._get_index_path()

        if os.path.exists(index_path):
            index = faiss.read_index(index_path)
            xids = np.array(
                [vector_data_instance.id for vector_data_instance in vector_data_instances]
            )

            index.remove_ids(xids)
            faiss.write_index(index, index_path)
            logger.info(f"Removed vector data for MultimodalVoidForgerChatMessage with ID {instance.id} from index.")
            print(f"Removed vector data for MultimodalVoidForgerChatMessage with ID {instance.id} from index.")

        else:
            print(f"Index path {index_path} does not exist.")

        for vector_data_instance in vector_data_instances:
            vector_data_instance.delete()

    except VoidForgerOldChatMessagesVectorData.DoesNotExist:
        print(
            f"No VoidForgerOldChatMessagesVectorData found for MultimodalVoidForgerChatMessage with ID {instance.id}.")
