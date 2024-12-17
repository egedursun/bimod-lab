#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_004c_knowledge_bases_create.py
#  Last Modified: 2024-12-11 23:19:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-11 23:19:20
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

from apps.datasource_knowledge_base.models import (
    DocumentKnowledgeBaseConnection
)

from apps.llm_core.models import (
    LLMCore
)

from apps.quick_setup_helper.utils import (
    generate_random_object_id_string
)

logger = logging.getLogger(__name__)


def action_004c_knowledge_bases_create(
    metadata__user,
    metadata__assistants,
):
    try:
        for assistant in metadata__assistants:
            assistant: Assistant

            try:
                metadata__llm_core: LLMCore
                DocumentKnowledgeBaseConnection.objects.create(
                    assistant=assistant,
                    name=f"Primary Document Knowledge Base for assistant {assistant.name} {generate_random_object_id_string()}",
                    description=f"This is the primary Document Knowledge Base connection for the assistant {assistant.name} and organization {assistant.organization.name}.",
                    vectorizer="text2vec-openai",
                    created_by_user=metadata__user,
                )

            except Exception as e:
                logger.error(
                    f"Failed to create Document Knowledge Base connection for assistant {assistant.name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__004c_knowledge_bases_create: {e}")

        return False

    logger.info("action__004c_knowledge_bases_create completed successfully.")

    return True
