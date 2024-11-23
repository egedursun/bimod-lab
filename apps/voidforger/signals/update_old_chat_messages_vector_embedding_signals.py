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

from apps.voidforger.models import MultimodalVoidForgerChatMessage, VoidForgerOldChatMessagesVectorData

logger = logging.getLogger(__name__)


@receiver(post_save, sender=MultimodalVoidForgerChatMessage)
def update_voidforger_old_chat_messages_vector_embedding_after_save(sender, instance, created, **kwargs):
    try:
        item, success = VoidForgerOldChatMessagesVectorData.objects.get_or_create(
            voidforger_chat_message=instance
        )

        if success:
            logger.info("VoidForgerOldChatMessagesVectorData created for MultimodalVoidForgerChatMessage.")

        else:
            logger.info("VoidForgerOldChatMessagesVectorData already exists; updating.")
            item.save()

    except Exception as e:
        logger.error(f"Error in post-save embedding update: {e}")
