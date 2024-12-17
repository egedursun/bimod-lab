#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_integration_embedding_signals.py
#  Last Modified: 2024-11-09 20:03:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-09 20:03:21
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

from django.db.models.signals import (
    pre_delete
)

from django.dispatch import receiver

from apps.integrations.models import (
    AssistantIntegration
)

from apps.semantor.models import (
    IntegrationVectorData
)

logger = logging.getLogger(__name__)


@receiver(pre_delete, sender=AssistantIntegration)
def remove_vector_from_index_on_integration_delete(
    sender,
    instance,
    **kwargs
):
    try:
        vector_data_instance = IntegrationVectorData.objects.get(
            integration_assistant=instance
        )

        index_path = vector_data_instance._get_index_path()

        if os.path.exists(index_path):
            index = faiss.read_index(index_path)
            xids = np.array(
                [
                    vector_data_instance.id
                ],
                dtype=np.int64
            )

            index.remove_ids(xids)

            faiss.write_index(
                index,
                index_path
            )

            logger.info(f"Removed vector data for AssistantIntegration with ID {instance.id} from index.")
        else:
            logger.warning(f"Index file not found for AssistantIntegration with ID {instance.id}.")

        vector_data_instance.delete()

    except IntegrationVectorData.DoesNotExist:
        logger.warning(f"No IntegrationVectorData found for AssistantIntegration with ID {instance.id}.")
