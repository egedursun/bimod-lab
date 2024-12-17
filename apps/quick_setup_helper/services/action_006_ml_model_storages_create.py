#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_006_ml_model_storages_create.py
#  Last Modified: 2024-11-18 20:52:49
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 20:52:50
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

from apps.assistants.models import Assistant

from apps.datasource_ml_models.models import (
    DataSourceMLModelConnection
)

from apps.datasource_ml_models.utils import (
    MLModelItemCategoriesNames
)

from apps.quick_setup_helper.utils import (
    generate_random_object_id_string
)

logger = logging.getLogger(__name__)


def action__006_ml_model_storages_create(
    metadata__assistants
):
    try:
        for assistant in metadata__assistants:
            assistant: Assistant

            try:
                DataSourceMLModelConnection.objects.create(
                    assistant=assistant,
                    name=f"{assistant.name}'s ML Model Storage {generate_random_object_id_string()}",
                    description=f"Primary Machine Learning Model Storage for assistant {assistant.name}",
                    model_object_category=MLModelItemCategoriesNames.PYTORCH,
                )

            except Exception as e:
                logger.error(f"Failed to create ML Model storage for assistant {assistant.name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__006_ml_model_storages_create: {str(e)}")

        return False

    logger.info("action__006_ml_model_storages_create completed successfully.")

    return True
