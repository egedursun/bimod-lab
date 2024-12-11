#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_analyze_code.py
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

from apps.core.code_analyst.code_interpreter_executor import (
    CodeAnalystExecutionManager
)

from apps.assistants.models import (
    Assistant
)

from apps.multimodal_chat.models import (
    MultimodalChat
)


logger = logging.getLogger(__name__)


def run_analyze_code(
    agent_id,
    chat_id,
    f_uris,
    query_content_str
):

    agent = Assistant.objects.get(
        id=agent_id
    )

    chat = MultimodalChat.objects.get(
        id=chat_id
    )

    xc = CodeAnalystExecutionManager(
        assistant=agent,
        chat=chat
    )

    try:

        output = xc.analyze_code_script(
            full_file_paths=f_uris,
            query_string=query_content_str
        )

        logger.info(f"Code analysis output: {output}")

    except Exception as e:
        logger.error(f"Error occurred while analyzing code: {e}")

        return None, None, None

    f_uris = output.get("file_uris")
    img_uris = output.get("image_uris")

    return output, f_uris, img_uris
