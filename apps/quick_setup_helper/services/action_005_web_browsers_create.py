#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_005_web_browsers_create.py
#  Last Modified: 2024-11-18 20:52:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 20:52:32
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
from apps.datasource_browsers.models import DataSourceBrowserConnection
from apps.datasource_browsers.utils import BrowserTypesNames
from apps.quick_setup_helper.utils import generate_random_object_id_string

logger = logging.getLogger(__name__)


def action__005_web_browsers_create(
    metadata__user,
    metadata__assistants
):
    try:
        for assistant in metadata__assistants:
            assistant: Assistant

            try:
                DataSourceBrowserConnection.objects.create(
                    assistant=assistant,
                    name=f"{assistant.name}'s Browser Connection {generate_random_object_id_string()}",
                    description=f"Primary Browser connection for assistant {assistant.name}",
                    browser_type=BrowserTypesNames.GOOGLE,
                    created_by_user=metadata__user
                )

            except Exception as e:
                logger.error(f"Failed to create browser connection for assistant {assistant.name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__005_web_browsers_create: {str(e)}")
        return False

    logger.info("action__005_web_browsers_create completed successfully.")
    return True
