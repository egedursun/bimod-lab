#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_integration_embedding_signals.py
#  Last Modified: 2024-11-09 19:58:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-09 19:58:16
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

from apps.integrations.models import AssistantIntegration

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AssistantIntegration)
def update_integration_embedding_after_save(sender, instance, created, **kwargs):
    from apps.semantor.models import IntegrationVectorData
    print("here...")
    try:
        item, success = IntegrationVectorData.objects.get_or_create(integration_assistant=instance)
        if success:
            logger.info("Integration vector data created for assistant integration.")
        else:
            logger.info("Integration vector data already exists; updating.")
            item.save()
    except Exception as e:
        logger.error(f"Error in post-save embedding update: {e}")
