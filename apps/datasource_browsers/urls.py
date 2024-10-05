#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.urls import path

from apps.datasource_browsers.views import CreateBrowserConnectionView, UpdateBrowserConnectionView, \
    DeleteBrowserConnectionView, ListBrowserConnectionsView, ListBrowsingLogsView, DownloadHtmlContentView, \
    DownloadContextDataView

app_name = "datasource_browsers"

urlpatterns = [
    path("create/", CreateBrowserConnectionView.as_view(
        template_name="datasource_browsers/connections/create_browser_connection.html"
    ), name="create"),
    path("update/<int:pk>/", UpdateBrowserConnectionView.as_view(
        template_name="datasource_browsers/connections/update_browser_connection.html"
    ), name="update"),
    path("delete/<int:pk>/", DeleteBrowserConnectionView.as_view(
        template_name="datasource_browsers/connections/confirm_delete_browser_connection.html"
    ), name="delete"),
    path("list/", ListBrowserConnectionsView.as_view(
        template_name="datasource_browsers/connections/list_browser_connections.html"
    ), name="list"),
    path("logs/<int:pk>/", ListBrowsingLogsView.as_view(
        template_name="datasource_browsers/logs/list_browser_logs.html"
    ), name="logs"),

    path('logs/download_html/<int:pk>/', DownloadHtmlContentView.as_view(), name='download_html'),
    path('logs/download_context/<int:pk>/', DownloadContextDataView.as_view(), name='download_context'),
]
