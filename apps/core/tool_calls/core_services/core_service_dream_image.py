#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_dream_image.py
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

from apps.core.tool_calls.utils import VISUALIZATION_TOOL_ERROR_LOG, VISUALIZATION_TOOL_STANDARD_ERROR_LOG
from apps.core.visual_client.operations import DreamManager
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat


logger = logging.getLogger(__name__)


def run_dream_image(
    agent_id,
    chat_id,
    img_uri,
    img_dimension
):

    agent = Assistant.objects.get(
        id=agent_id
    )

    chat = MultimodalChat.objects.get(
        id=chat_id
    )

    xc = DreamManager(
        assistant=agent,
        chat=chat
    )

    if agent.image_generation_capability is False:
        logger.error("The agent does not have the capability to generate images.")
        return VISUALIZATION_TOOL_ERROR_LOG

    try:
        logger.info(f"Running dream image generation for the agent: {agent} and chat: {chat}")
        output = xc.dream_image_execution_manager(
            image_uri=img_uri,
            image_size=img_dimension
        )

    except Exception as e:
        logger.error(f"Error occurred while running the dream image generation: {e}")
        error = VISUALIZATION_TOOL_STANDARD_ERROR_LOG
        return error

    logger.info(f"Dream image generation output: {output}")
    return output
