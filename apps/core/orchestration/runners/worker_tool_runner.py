#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: worker_tool_runner.py
#  Last Modified: 2024-10-05 02:26:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
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

from apps.orchestrations.models import (
    OrchestrationQuery,
    Maestro
)

logger = logging.getLogger(__name__)


def run_worker_tool(
    maestro_id,
    query_id,
    worker_assistant_id,
    query_text,
    file_urls,
    image_urls
):
    from apps.core.orchestration.orchestration_executor import (
        OrchestrationExecutor
    )

    from apps.core.orchestration.utils import (
        DEFAULT_WORKER_ASSISTANT_ERROR_MESSAGE
    )

    maestro = Maestro.objects.get(
        id=maestro_id
    )

    query_chat = OrchestrationQuery.objects.get(
        id=query_id
    )

    try:
        executor = OrchestrationExecutor(
            maestro=maestro,
            query_chat=query_chat,
        )
        logger.info('[worker_tool_runner.run_worker_tool] The executor is created successfully.')

    except Exception as e:
        logger.error('[worker_tool_runner.run_worker_tool] An error occurred while creating the executor:', e)

        return DEFAULT_WORKER_ASSISTANT_ERROR_MESSAGE

    try:
        final_response = executor.ask_worker_assistant(
            assistant_id=worker_assistant_id,
            maestro_query=query_text,
            file_urls=file_urls,
            image_urls=image_urls,
        )

        logger.info('[worker_tool_runner.run_worker_tool] The worker assistant is asked successfully.')

    except Exception as e:
        logger.error('[worker_tool_runner.run_worker_tool] An error occurred while asking the worker assistant:', e)

        return DEFAULT_WORKER_ASSISTANT_ERROR_MESSAGE

    logger.info('[worker_tool_runner.run_worker_tool] The worker assistant is asked successfully.')

    return final_response
