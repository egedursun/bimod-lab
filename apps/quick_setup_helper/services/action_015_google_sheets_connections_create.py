#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_015_google_sheets_connections_create.py
#  Last Modified: 2024-11-18 22:25:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:25:15
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

from apps.sheetos.models import (
    SheetosGoogleAppsConnection
)

from apps.sheetos.utils import (
    generate_google_apps_connection_api_key
)

logger = logging.getLogger(__name__)


def action__015_google_sheets_connections_create(
    metadata__user,
    metadata__assistants
):
    try:
        for assistant in metadata__assistants:
            assistant: Assistant

            try:
                SheetosGoogleAppsConnection.objects.create(
                    sheetos_assistant=assistant,
                    owner_user=metadata__user,
                    connection_api_key=generate_google_apps_connection_api_key()
                )

            except Exception as e:
                logger.error(
                    f"Failed to create Sheetos Google Apps Connection for assistant {assistant.name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__015_google_sheets_connections_create: {str(e)}")

        return False

    logger.info("action__015_google_sheets_connections_create completed successfully.")

    return True
