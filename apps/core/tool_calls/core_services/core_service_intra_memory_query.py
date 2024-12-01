#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_intra_memory_query.py
#  Last Modified: 2024-10-05 02:31:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
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

from apps.core.context_memory_manager.context_memory_manager import ContextMemoryManager


logger = logging.getLogger(__name__)


def run_query_intra_memory(
    assistant_chat_id: int,
    intra_memory_query: str
):

    try:

        output = ContextMemoryManager.search_old_chat_messages(
            assistant_chat_id=assistant_chat_id,
            query=intra_memory_query
        )

    except Exception as e:
        logger.error(f"Error occurred while executing the Assistant message memory query: {e}")
        error_msg = f"Error occurred while executing the Assistant message memory query: {str(e)}"
        return error_msg

    return output
