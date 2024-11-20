#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_021_export_assistants_create.py
#  Last Modified: 2024-11-18 22:26:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:26:38
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
from apps.export_assistants.models import ExportAssistantAPI

logger = logging.getLogger(__name__)


def action__021_export_assistants_create(
    metadata__user,
    metadata__organization,
    metadata__assistants
):
    try:
        for assistant in metadata__assistants:
            assistant: Assistant

            try:

                ExportAssistantAPI.objects.create(
                    organization=metadata__organization,
                    assistant=assistant,
                    created_by_user=metadata__user
                )

            except Exception as e:
                logger.error(f"Failed to create Export Assistant API for assistant {assistant.name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__021_export_assistants_create: {str(e)}")
        return False

    logger.info("action__021_export_assistants_create completed successfully.")
    return True
