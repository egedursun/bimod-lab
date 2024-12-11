#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_generate_image.py
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

from apps.core.tool_calls.utils import (
    VISUALIZATION_TOOL_ERROR_LOG,
    VISUALIZATION_TOOL_STANDARD_ERROR_LOG
)

from apps.core.visual_client.operations import (
    GeneratorManager
)

from apps.assistants.models import Assistant

from apps.multimodal_chat.models import (
    MultimodalChat
)

logger = logging.getLogger(__name__)


def run_generate_image(
    agent_id,
    chat_id,
    img_generation_prompt,
    img_dimensions,
    img_resolution
):
    agent = Assistant.objects.get(
        id=agent_id
    )

    chat = MultimodalChat.objects.get(
        id=chat_id
    )

    xc = GeneratorManager(
        assistant=agent,
        chat=chat
    )

    if agent.image_generation_capability is False:
        logger.error("The agent does not have the capability to generate images.")

        return VISUALIZATION_TOOL_ERROR_LOG

    try:

        output = xc.generate_image_execution_manager(
            prompt=img_generation_prompt,
            image_size=img_dimensions,
            quality=img_resolution
        )

        logger.info(f"Image generation output: {output}")

    except Exception as e:
        logger.error(f"Error occurred while running the image generation: {e}")
        error = VISUALIZATION_TOOL_STANDARD_ERROR_LOG

        return error

    return output
