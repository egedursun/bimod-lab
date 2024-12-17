#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_011_metatempo_tracker_create.py
#  Last Modified: 2024-11-18 22:24:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:24:33
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
import secrets

from apps.assistants.models import Assistant

from apps.metatempo.models import (
    MetaTempoConnection,
    MetaTempoAssistantConnection
)

from apps.quick_setup_helper.utils import (
    generate_random_object_id_string
)

from apps.metatempo.utils import (
    META_TEMPO_CONNECTION_API_KEY_DEFAULT_LENGTH
)

logger = logging.getLogger(__name__)


def action__011_metatempo_tracker_create(
    metadata__user,
    metadata__metakanban_board,
    metadata__assistants
):
    try:
        connection_api_key = str(
            secrets.token_urlsafe(
                META_TEMPO_CONNECTION_API_KEY_DEFAULT_LENGTH
            )
        )

        new_metatempo_item = MetaTempoConnection.objects.create(
            board=metadata__metakanban_board,
            optional_context_instructions=f"MetaTempo Team Performance and Metrics Tracker for {metadata__metakanban_board} {generate_random_object_id_string()}",
            tracked_weekdays=[
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday"
            ],
            tracking_start_time=None,
            tracking_end_time=None,
            created_by_user=metadata__user,
            connection_api_key=connection_api_key
        )

    except Exception as e:
        logger.error(f"Error in action__011_metatempo_tracker_create: {e}")

        return False, None

    # Connect MetaTempo tracker to Assistants

    try:
        for assistant in metadata__assistants:
            assistant: Assistant

            MetaTempoAssistantConnection.objects.create(
                assistant=assistant,
                metatempo_instance=new_metatempo_item,
                created_by_user=metadata__user
            )

    except Exception as e:
        logger.error(f"Error while connecting assistants to the new MetaTempo board: {e}")

        return False, None

    logger.info(f"New MetaTempo tracker created successfully: {new_metatempo_item}")

    return True, new_metatempo_item
