#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_004a_website_storages_create.py
#  Last Modified: 2024-12-09 14:59:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-09 14:59:40
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

from apps.datasource_website.models import (
    DataSourceWebsiteStorageConnection
)

from apps.quick_setup_helper.utils import (
    generate_random_object_id_string
)

logger = logging.getLogger(__name__)


def action__004a_website_storages_create(
    metadata__user,
    metadata__assistants,
    metadata__maximum__pages_to_index
):
    try:
        for assistant in metadata__assistants:
            assistant: Assistant

            try:

                DataSourceWebsiteStorageConnection.objects.create(
                    assistant=assistant,
                    name=f"{assistant.name}'s Website Storage {generate_random_object_id_string()}",
                    description=f"This is the default website storage for the assistant {assistant.name}.",
                    vectorizer="text2vec-openai",
                    embedding_chunk_size=2000,
                    embedding_chunk_overlap=1000,
                    search_instance_retrieval_limit=10,
                    maximum_pages_to_index=metadata__maximum__pages_to_index,
                    created_by_user=metadata__user
                )

            except Exception as e:
                logger.error(f"Error while creating website storage connection for assistant {assistant.name}: {e}")
                continue

    except Exception as e:
        logger.error(f"Error while creating website storage connection: {e}")

        return False

    logger.info("action__004a_website_storages_create completed successfully.")

    return True
