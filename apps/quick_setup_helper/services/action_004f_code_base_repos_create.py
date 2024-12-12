#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_004f_code_base_repos_create.py
#  Last Modified: 2024-12-11 23:20:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-11 23:20:06
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

from apps.assistants.models import (
    Assistant
)

from apps.datasource_codebase.models import (
    CodeBaseRepository
)

from apps.datasource_codebase.tasks import (
    load_and_index_repository
)

logger = logging.getLogger(__name__)


def action__004f_code_base_repos_create(
    metadata__user,
    metadata__repository_urls,
    metadata__assistants,
):
    try:

        for assistant in metadata__assistants:
            assistant: Assistant

            try:

                vector_store = assistant.coderepositorystorageconnection_set.first()

                if vector_store and metadata__repository_urls and len(metadata__repository_urls) > 0:

                    for repository_url in metadata__repository_urls:

                        # Save the Code Repository object
                        new_repository = CodeBaseRepository.objects.create(
                            knowledge_base=vector_store,
                            repository_uri=repository_url,
                            repository_name=repository_url.split('/')[-1],
                            repository_description="Automatically created by quick setup. Code base repository for assistant " + assistant.name + ", created by " + metadata__user.email,
                            created_by_user=metadata__user,
                        )

                        new_repository.save()

                        success = load_and_index_repository(
                            item_id=new_repository.id
                        )

                        if not success:
                            logger.error('Error while indexing Code Repositories.')
                            continue

            except Exception as e:
                logger.error(f"Error while creating Code Repositories for assistant {assistant.name}: {e}")

                return False

    except Exception as e:
        logger.error(f"Error while creating Code Repositories: {e}")

        return False

    logger.info("action__004f_code_base_repos_create has been executed successfully.")

    return True
