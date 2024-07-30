from django.urls import path

from apps.datasource_browsers.views import CreateBrowserConnectionView, UpdateBrowserConnectionView, \
    DeleteBrowserConnectionView, ListBrowserConnectionsView, ListBrowsingLogsView, DownloadHtmlContentView, \
    DownloadContextDataView

app_name = "datasource_browsers"


urlpatterns = [
    path("create/", CreateBrowserConnectionView.as_view(
        template_name="datasource_browsers/create_browser_connection.html"
    ), name="create"),
    path("update/<int:pk>/", UpdateBrowserConnectionView.as_view(
        template_name="datasource_browsers/update_browser_connection.html"
    ), name="update"),
    path("delete/<int:pk>/", DeleteBrowserConnectionView.as_view(
        template_name="datasource_browsers/confirm_delete_browser_connection.html"
    ), name="delete"),
    path("list/", ListBrowserConnectionsView.as_view(
        template_name="datasource_browsers/list_browser_connections.html"
    ), name="list"),
    path("logs/<int:pk>/", ListBrowsingLogsView.as_view(
        template_name="datasource_browsers/list_browser_logs.html"
    ), name="logs"),
    ############################################################################################################
    path('logs/download_html/<int:pk>/', DownloadHtmlContentView.as_view(), name='download_html'),
    path('logs/download_context/<int:pk>/', DownloadContextDataView.as_view(), name='download_context'),
]
