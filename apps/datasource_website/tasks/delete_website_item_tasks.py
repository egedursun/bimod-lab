#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_website_item_tasks.py
#  Last Modified: 2024-12-09 02:53:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-09 02:53:32
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

from apps.datasource_website.models import (
    DataSourceWebsiteStorageItem
)

from apps.datasource_website.tasks import (
    clean_previous_data
)

logger = logging.getLogger(__name__)


def handle_delete_website_item(item: DataSourceWebsiteStorageItem):
    try:
        success = clean_previous_data(item=item)

        if success is False:
            logger.error(f"An error occurred while deleting the data for website item with ID: {item.id}")

            return False

        item.delete()

        logger.info(f"Successfully deleted the data for website item with ID: {item.id}")
        return True

    except Exception as e:
        logger.error(f"An error occurred while deleting the data for website item with ID: {item.id}")

        return False
