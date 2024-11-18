#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_old_leanmod_chat_messages_vector_embedding_signals.py
#  Last Modified: 2024-11-17 20:31:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-17 20:49:59
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

from apps.leanmod.models import LeanModOldChatMessagesVectorData
from apps.multimodal_chat.models import MultimodalLeanChatMessage

logger = logging.getLogger(__name__)


@receiver(pre_delete, sender=MultimodalLeanChatMessage)
def remove_vector_from_index_on_leanmod_chat_message_delete(sender, instance, **kwargs):
    try:
        vector_data_instances = LeanModOldChatMessagesVectorData.objects.filter(
            leanmod_chat_message=instance
        ).all()
        if not vector_data_instances:
            print(f"No vector data found for MultimodalLeanChatMessage with ID {instance.id}.")
            return

        index_path = vector_data_instances[0]._get_index_path()
        if os.path.exists(index_path):
            index = faiss.read_index(index_path)
            xids = np.array([vector_data_instance.id for vector_data_instance in vector_data_instances])
            index.remove_ids(xids)
            faiss.write_index(index, index_path)
            logger.info(f"Removed vector data for MultimodalLeanChatMessage with ID {instance.id} from index.")
            print(f"Removed vector data for MultimodalLeanChatMessage with ID {instance.id} from index.")
        else:
            print(f"Index path {index_path} does not exist.")
        for vector_data_instance in vector_data_instances:
            vector_data_instance.delete()
    except LeanModOldChatMessagesVectorData.DoesNotExist:
        print(
            f"No LeanModOldChatMessagesVectorData found for MultimodalLeanChatMessage with ID {instance.id}.")
