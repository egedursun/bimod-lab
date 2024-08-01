

def execute_browser_action(connection_id, action, query, page, search_results, click_url):
    from apps._services.browsers.browser_executor import BrowsingExecutor, BrowserActionsNames
    from apps.datasource_browsers.models import DataSourceBrowserConnection

    connection = DataSourceBrowserConnection.objects.get(id=connection_id)
    executor = BrowsingExecutor(connection=connection)

    if action == BrowserActionsNames.BROWSER_SEARCH:
        return executor.act(BrowserActionsNames.BROWSER_SEARCH, query=query, page=page)
    elif action == BrowserActionsNames.CLICK_URL_IN_SEARCH:
        return executor.act(BrowserActionsNames.CLICK_URL_IN_SEARCH, search_results=search_results, click_url=click_url)
    else:
        return f"[browser_execution_tool_handler.execute_browser_action] Invalid action: {action}. Must be one of {BrowserActionsNames.as_list()}."
