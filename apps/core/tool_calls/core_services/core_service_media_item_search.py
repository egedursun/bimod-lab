#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_media_item_search.py
#  Last Modified: 2024-12-01 23:14:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-01 23:14:14
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

from apps.core.media_managers.media_manager_execution_handler import MediaManager
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection

logger = logging.getLogger(__name__)


def run_query_search_media_items(
    connection_id: str,
    chat,
    query: str
):
    try:
        connection = DataSourceMediaStorageConnection.objects.get(id=connection_id)
        if not connection:
            return f"Connection with ID: {connection_id} does not exist."

        xc = MediaManager(
            connection=connection,
            chat=chat
        )
        output = xc.search_media_items(query=query)

    except Exception as e:
        logger.error(f"Error occurred while executing the Media Item Search query: {str(e)}")
        error_msg = f"Error occurred while executing the Media Item Search query: {str(e)}"
        return error_msg

    return output
