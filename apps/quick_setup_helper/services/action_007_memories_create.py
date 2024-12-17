#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_007_memories_create.py
#  Last Modified: 2024-11-18 20:56:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 20:56:41
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
from apps.memories.models import AssistantMemory

from apps.memories.utils import (
    AgentStandardMemoryTypesNames
)

logger = logging.getLogger(__name__)


def action__007_memories_create(
    metadata__user,
    metadata__organization,
    metadata__assistants,
    response__assistant_notes
):
    try:
        for assistant in metadata__assistants:
            assistant: Assistant

            try:

                for note in response__assistant_notes:
                    AssistantMemory.objects.create(
                        user=metadata__user,
                        assistant=assistant,
                        organization=metadata__organization,
                        memory_type=AgentStandardMemoryTypesNames.ASSISTANT_SPECIFIC,
                        memory_text_content=note
                    )

            except Exception as e:
                logger.error(f"Failed to create memory notes for for assistant {assistant.name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__007_memories_create: {str(e)}")

        return False

    logger.info("action__007_memories_create completed successfully.")

    return True
