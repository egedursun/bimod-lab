

def execute_browser_action(connection_id, action, query, page, search_results, click_url):
    from apps._services.browsers.browser_executor import BrowsingExecutor, ActionsNames
    from apps.datasource_browsers.models import DataSourceBrowserConnection

    connection = DataSourceBrowserConnection.objects.get(id=connection_id)
    executor = BrowsingExecutor(connection=connection)

    if action == "browser_search":
        return executor.act("browser_search", query=query, page=page)
    elif action == "click_url_in_search":
        return executor.act("click_url_in_search", search_results=search_results, click_url=click_url)
    else:
        return f"Invalid action: {action}. Must be one of {ActionsNames.as_list()}."
