#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_023_export_orchestrations_create.py
#  Last Modified: 2024-11-18 22:26:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:27:00
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

from apps.export_orchestrations.models import ExportOrchestrationAPI
from apps.orchestrations.models import Maestro

logger = logging.getLogger(__name__)


def action__023_export_orchestrations_create(
    metadata__user,
    metadata__organization,
    metadata__orchestrators
):
    try:
        for orchestrator_assistant in metadata__orchestrators:
            orchestrator_assistant: Maestro

            try:

                ExportOrchestrationAPI.objects.create(
                    organization=metadata__organization,
                    orchestrator=orchestrator_assistant,
                    created_by_user=metadata__user
                )

            except Exception as e:
                logger.error(
                    f"Failed to create Export Orchestrator Maestro API for orchestrator {orchestrator_assistant.name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__023_export_orchestrations_create: {str(e)}")
        return False

    logger.info("action__023_export_orchestrations_create completed successfully.")
    return True
