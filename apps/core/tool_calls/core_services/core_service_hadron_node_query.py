#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_hadron_node_query.py
#  Last Modified: 2024-11-13 05:09:44
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 05:11:00
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

from apps.core.hadron_prime.hadron_prime_executor import (
    HadronPrimeExecutor
)

from apps.hadron_prime.models import (
    HadronNodeAssistantConnection
)

logger = logging.getLogger(__name__)


def run_query_execute_hadron_node(
    c_id: int,
    query: str
):
    try:

        connection = HadronNodeAssistantConnection.objects.get(
            id=c_id
        )

        xc = HadronPrimeExecutor(
            node=connection.hadron_prime_node,
            execution_log_object=None
        )

        output, success, error = xc.generate_node_speech(
            user_query_text=query
        )

        if error:
            logger.error(f"Error occurred while running the Hadron Node Query execution tool: {error}")

            return error

    except Exception as e:
        logger.error(f"Error occurred while running the Hadron Node Query execution tool: {e}")
        error = f"There has been an unexpected error on running the Hadron Node Query execution tool: {e}"

        return error

    return output
