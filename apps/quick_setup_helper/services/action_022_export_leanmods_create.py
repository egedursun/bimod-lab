#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_022_export_leanmods_create.py
#  Last Modified: 2024-11-18 22:26:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:26:49
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

from apps.export_leanmods.models import (
    ExportLeanmodAssistantAPI
)

from apps.leanmod.models import LeanAssistant

logger = logging.getLogger(__name__)


def action__022_export_leanmods_create(
    metadata__user,
    metadata__organization,
    metadata__leanmods
):
    try:
        for lean_assistant in metadata__leanmods:
            lean_assistant: LeanAssistant

            try:

                ExportLeanmodAssistantAPI.objects.create(
                    organization=metadata__organization,
                    lean_assistant=lean_assistant,
                    created_by_user=metadata__user
                )

            except Exception as e:
                logger.error(
                    f"Failed to create Export LeanMod Assistant API for assistant {lean_assistant.name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__022_export_leanmods_create: {str(e)}")

        return False

    logger.info("action__022_export_leanmods_create completed successfully.")

    return True
