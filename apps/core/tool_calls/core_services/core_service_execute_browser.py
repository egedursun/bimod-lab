#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_execute_browser.py
#  Last Modified: 2024-10-05 02:26:00
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

logger = logging.getLogger(__name__)


def run_execute_browsing(
    connection_id,
    browsing_action,
    browsing_query,
    page_definition,
    search_results,
    click_url
):

    from apps.core.browsers.browser_executor import BrowsingExecutor
    from apps.core.browsers.utils import BrowserActionsNames
    from apps.datasource_browsers.models import DataSourceBrowserConnection

    conn = DataSourceBrowserConnection.objects.get(
        id=connection_id
    )

    xc = BrowsingExecutor(
        connection=conn
    )

    if browsing_action == BrowserActionsNames.BROWSER_SEARCH:

        logger.info(f"Running browsing action: {browsing_action} with query: {browsing_query}")
        return xc.act(
            BrowserActionsNames.BROWSER_SEARCH,
            query=browsing_query,
            page=page_definition
        )

    elif browsing_action == BrowserActionsNames.CLICK_URL_IN_SEARCH:

        logger.info(f"Running browsing action: {browsing_action} with search results: {search_results} and click url: {click_url}")
        return xc.act(
            BrowserActionsNames.CLICK_URL_IN_SEARCH,
            search_results=search_results,
            click_url=click_url
        )

    else:

        logger.error(f"Invalid action: {browsing_action}. Must be one of {BrowserActionsNames.as_list()}.")
        action_error_log = f"Invalid action: {browsing_action}. Must be one of {BrowserActionsNames.as_list()}."
        return action_error_log
