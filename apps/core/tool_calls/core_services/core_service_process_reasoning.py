#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_process_reasoning.py
#  Last Modified: 2024-10-06 20:31:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-06 20:31:27
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

from apps.core.reasoning.reasoning_executor import ReasoningExecutor
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat


logger = logging.getLogger(__name__)


def run_process_reasoning(
    agent_id,
    chat_id,
    reasoning_query
):

    agent = Assistant.objects.get(
        id=agent_id
    )

    chat = MultimodalChat.objects.get(
        id=chat_id
    )

    xc = ReasoningExecutor(
        assistant=agent,
        chat=chat
    )

    output = None
    try:
        output = xc.execute_process_reasoning(
            query_string=reasoning_query
        )

    except Exception as e:
        logger.error(f"Error occurred while processing the reasoning: {e}")
        return f"Failed to process the reasoning. The cause of the error is as follows: {str(e)}"

    logger.info(f"Reasoning output: {output}")
    return output
