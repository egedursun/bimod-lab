#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_leanmod_assistant_embedding_signals.py
#  Last Modified: 2024-11-15 23:56:52
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 23:56:53
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

from django.db.models.signals import (
    post_save
)

from django.dispatch import receiver

from apps.leanmod.models import LeanAssistant

from apps.semantor.models import (
    LeanModVectorData
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=LeanAssistant)
def update_leanmod_assistant_embedding_after_save(
    sender,
    instance,
    created,
    **kwargs
):
    try:
        item, success = LeanModVectorData.objects.get_or_create(
            leanmod_assistant=instance
        )

        if success:
            logger.info("LeanAssistant vector data created for assistant.")

        else:
            logger.info("LeanAssistant vector data already exists; updating.")

            item.save()

    except Exception as e:
        logger.error(f"Error in post-save embedding update: {e}")
