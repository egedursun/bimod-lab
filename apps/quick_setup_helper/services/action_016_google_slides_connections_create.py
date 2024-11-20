#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_016_google_slides_connections_create.py
#  Last Modified: 2024-11-18 22:25:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:25:28
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

from apps.assistants.models import Assistant
from apps.slider.models import SliderGoogleAppsConnection
from apps.slider.utils import generate_google_apps_connection_api_key

logger = logging.getLogger(__name__)


def action__016_google_slides_connections_create(
    metadata__user,
    metadata__assistants
):
    try:
        for assistant in metadata__assistants:
            assistant: Assistant

            try:
                SliderGoogleAppsConnection.objects.create(
                    slider_assistant=assistant,
                    owner_user=metadata__user,
                    connection_api_key=generate_google_apps_connection_api_key()
                )

            except Exception as e:
                logger.error(
                    f"Failed to create Slider Google Apps Connection for assistant {assistant.name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__016_google_slides_connections_create: {str(e)}")
        return False

    logger.info("action__016_google_slides_connections_create completed successfully.")
    return True
