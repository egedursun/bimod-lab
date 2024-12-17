#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_004b_website_items_create.py
#  Last Modified: 2024-12-09 15:02:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-09 15:02:05
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

from apps.datasource_website.models import (
    DataSourceWebsiteStorageItem
)

from apps.datasource_website.tasks import (
    crawl_and_index_website_item
)

from apps.datasource_website.utils import (
    WebsiteIndexingMethodologyChoicesNames
)

logger = logging.getLogger(__name__)


def action__004b_website_items_create(
    metadata__user,
    metadata__website_urls,
    metadata__assistants
):
    try:

        for assistant in metadata__assistants:
            assistant: Assistant

            try:

                for website_url in metadata__website_urls:
                    new_website_item = DataSourceWebsiteStorageItem.objects.create(
                        storage=assistant.datasourcewebsitestorageconnection_set.first(),
                        website_url=website_url,
                        crawling_methodology=WebsiteIndexingMethodologyChoicesNames.HTML_CONTENT,
                        created_by_user=metadata__user
                    )

                    # Crawl and index the website item.

                    crawl_and_index_website_item(
                        item_id=new_website_item.id,
                        delete_previous=False
                    )

            except Exception as e:
                logger.error(f"Error while creating website items for assistant {assistant.name}: {e}")

    except Exception as e:
        logger.error(f"Error while creating website items: {e}")

        return False

    logger.info("action__004b_website_items_create completed successfully.")

    return True
