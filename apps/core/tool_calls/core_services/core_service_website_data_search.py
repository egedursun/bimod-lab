#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_website_data_search.py
#  Last Modified: 2024-12-09 01:59:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-09 01:59:38
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
import traceback

from apps.core.website.website_executor import WebsiteExecutionManager
from apps.datasource_website.models import (
    DataSourceWebsiteStorageConnection
)

logger = logging.getLogger(__name__)


def run_query_search_website_data(
    connection_id: str,
    website_url: str,
    query: str
):
    try:
        connection = DataSourceWebsiteStorageConnection.objects.get(id=connection_id)
        if not connection:
            return f"Connection with ID: {connection_id} does not exist."

        xc = WebsiteExecutionManager(
            connection_id=connection_id
        )

        output = xc.search_within_website_item_chunks(
            website_url=website_url,
            query=query
        )

    except Exception as e:
        logger.error(f"Error occurred while executing the Website Data Search query: {str(e)}")
        logger.error(traceback.format_exc())
        error_msg = f"Error occurred while executing the Website Data Search query: {str(e)}"
        return error_msg

    return output
