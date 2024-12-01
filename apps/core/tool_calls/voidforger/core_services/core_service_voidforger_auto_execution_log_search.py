#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_voidforger_auto_execution_log_search.py
#  Last Modified: 2024-11-16 00:35:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:35:58
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

logger = logging.getLogger(__name__)


def execute_voidforger_auto_execution_log_search_query(
    user,
    voidforger_id,
    query
):

    from apps.core.voidforger.voidforger_executor import VoidForgerExecutionManager

    try:
        xc = VoidForgerExecutionManager(
            user=user,
            voidforger_id=voidforger_id
        )

        search_output = xc.search_auto_execution_logs(
            query=query
        )

        logger.info(f"VoidForger auto-execution logs search query output: {search_output}")

    except Exception as e:
        logger.error(f"Error occurred while executing the function: {e}")
        error = f"Error occurred while executing the function: {str(e)}"
        return error

    return search_output
