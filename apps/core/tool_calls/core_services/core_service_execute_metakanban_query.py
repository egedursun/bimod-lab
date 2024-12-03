#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_execute_metakanban_query.py
#  Last Modified: 2024-11-13 05:09:03
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

from apps.core.metakanban.metakanban_execution_handler import (
    MetaKanbanExecutionManager
)

from apps.metakanban.models import MetaKanbanAssistantConnection

logger = logging.getLogger(__name__)


def run_query_execute_metakanban(
    c_id: int,
    query: str
):

    try:

        connection = MetaKanbanAssistantConnection.objects.get(
            id=c_id
        )

        xc = MetaKanbanExecutionManager(
            board_id=connection.metakanban_board.id
        )

        success, output = xc.consult_ai(
            user_query=query
        )

        if success is False:
            error = f"There has been an unexpected error on running the MetaKanban board manager AI query: {output}"
            return error

    except Exception as e:
        logger.error(f"Error occurred while running the MetaKanban board manager AI query: {e}")
        error = f"There has been an unexpected error on running the MetaKanban board manager AI query: {e}"
        return error

    return output
