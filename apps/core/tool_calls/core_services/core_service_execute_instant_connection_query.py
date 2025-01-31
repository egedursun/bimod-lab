#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_execute_instant_connection_query.py
#  Last Modified: 2025-01-28 15:47:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-01-28 15:47:05
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

from apps.core.instant_connector.instant_connector_execution_manager import (
    InstantConnectionExecutionManager
)

logger = logging.getLogger(__name__)


def run_instant_connection_query(
    assistant: Assistant,
    connection_string: str,
    query_command: str
):
    try:
        client: InstantConnectionExecutionManager = InstantConnectionExecutionManager(
            connection_string=connection_string
        )

        logger.info(f"Executing Instant Connection query: {query_command}")

        query_command_response = client.execute_query_or_command(
            assistant=assistant,
            query_command=query_command
        )

    except Exception as e:
        logger.error(f"Error occurred while executing the Instant Connection query: {str(e)}")
        error_msg = f"Error occurred while executing the Instant Connection query: {str(e)}"

        return error_msg

    logger.info(f"Instant Connection query executed successfully: {query_command_response}")

    return query_command_response
