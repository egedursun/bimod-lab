#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_old_media_item_vector_embedding_signals.py
#  Last Modified: 2024-12-01 23:31:56
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-02 00:27:33
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

from apps.datasource_media_storages.models import (
    DataSourceMediaStorageItem,
    MediaItemVectorData
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=DataSourceMediaStorageItem)
def update_media_item_vector_embedding_after_save(
    sender,
    instance,
    created,
    **kwargs
):
    try:
        item, success = MediaItemVectorData.objects.get_or_create(
            media_item=instance
        )

        if success:
            logger.info("MediaItemVectorData created for DataSourceMediaStorageItem.")

        else:
            logger.info("MediaItemVectorData already exists; updating.")
            item.save()

    except Exception as e:
        logger.error(f"Error in post-save embedding update: {e}")
