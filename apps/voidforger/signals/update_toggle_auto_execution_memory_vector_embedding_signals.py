#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_toggle_auto_execution_memory_vector_embedding_signals.py
#  Last Modified: 2024-11-16 05:46:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 05:46:34
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

from apps.voidforger.models import VoidForgerAutoExecutionMemoryVectorData, VoidForgerToggleAutoExecutionLog

logger = logging.getLogger(__name__)


@receiver(post_save, sender=VoidForgerToggleAutoExecutionLog)
def update_voidforger_toggle_auto_execution_memory_vector_embedding_after_save(sender, instance, created, **kwargs):
    try:
        item, success = VoidForgerAutoExecutionMemoryVectorData.objects.get_or_create(
            voidforger_auto_execution_memory=instance
        )

        if success:
            logger.info("VoidForgerAutoExecutionMemoryVectorData created for VoidForgerToggleAutoExecutionLog.")

        else:
            logger.info("VoidForgerAutoExecutionMemoryVectorData already exists; updating.")
            item.save()

    except Exception as e:
        logger.error(f"Error in post-save embedding update: {e}")
