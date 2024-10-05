#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: browser_execution_tool_handler.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: browser_execution_tool_handler.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:14:05
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

def execute_browser_action(connection_id, action, query, page, search_results, click_url):
    from apps._services.browsers.browser_executor import BrowsingExecutor
    from apps._services.browsers.utils import BrowserActionsNames
    from apps.datasource_browsers.models import DataSourceBrowserConnection

    connection = DataSourceBrowserConnection.objects.get(id=connection_id)
    executor = BrowsingExecutor(connection=connection)
    print(f"[browser_execution_tool_handler.execute_browser_action] Executing action: {action}.")

    if action == BrowserActionsNames.BROWSER_SEARCH:
        print(f"[browser_execution_tool_handler.execute_browser_action] Searching for: {query}.")
        return executor.act(BrowserActionsNames.BROWSER_SEARCH, query=query, page=page)
    elif action == BrowserActionsNames.CLICK_URL_IN_SEARCH:
        print(f"[browser_execution_tool_handler.execute_browser_action] Clicking on URL: {click_url}.")
        return executor.act(BrowserActionsNames.CLICK_URL_IN_SEARCH, search_results=search_results,
                            click_url=click_url)
    else:
        return f"[browser_execution_tool_handler.execute_browser_action] Invalid action: {action}. Must be one of {BrowserActionsNames.as_list()}."
