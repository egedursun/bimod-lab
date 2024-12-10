#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_old_chat_messages_vector_embedding_signals.py
#  Last Modified: 2024-11-16 05:46:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 05:46:22
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

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.assistants.models import (
    AssistantOldChatMessagesVectorData
)

from apps.multimodal_chat.models import (
    MultimodalChatMessage
)

logger = logging.getLogger(__name__)


@receiver(
    post_save,
    sender=MultimodalChatMessage
)
def update_assistant_old_chat_messages_vector_embedding_after_save(
    sender,
    instance,
    created,
    **kwargs
):
    try:
        item, success = AssistantOldChatMessagesVectorData.objects.get_or_create(
            assistant_chat_message=instance
        )

        if success:
            logger.info("AssistantOldChatMessagesVectorData created for MultimodalChatMessage.")

        else:
            logger.info("AssistantOldChatMessagesVectorData already exists; updating.")
            item.save()

    except Exception as e:
        logger.error(f"Error in post-save embedding update: {e}")
