#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_execute_metatempo_query.py
#  Last Modified: 2024-11-13 05:09:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 05:10:57
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

from apps.core.metatempo.metatempo_execution_handler import (
    MetaTempoExecutionManager
)

from apps.metatempo.models import MetaTempoAssistantConnection

logger = logging.getLogger(__name__)


def run_query_execute_metatempo(
    c_id: int,
    action: str,
    query: str
):

    try:
        connection = MetaTempoAssistantConnection.objects.get(
            id=c_id
        )

        xc = MetaTempoExecutionManager(
            metatempo_connection_id=connection.metatempo_instance.id
        )

        if action == "QUERY":
            output, error = xc.answer_logs_question(
                user_query=query
            )

            if error:
                logger.error(f"Error occurred while running the MetaTempo board manager AI 'QUERY' query: {error}")
                return error

        elif action == "REPORT":
            output, error = xc.interpret_overall_logs()

            if error:
                logger.error(f"Error occurred while running the MetaTempo board manager AI 'REPORT' query: {error}")
                return error

        else:
            error = f"Invalid action type: {action}"
            logger.error(f"Error occurred while running the MetaTempo board manager AI query: {error}")
            return error

    except Exception as e:
        logger.error(f"Error occurred while running the MetaTempo board manager AI query: {e}")
        error = f"There has been an unexpected error on running the MetaTempo board manager AI query: {e}"
        return error

    return output
