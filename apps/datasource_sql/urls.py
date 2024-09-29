#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-08-09 02:41:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:49:47
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.datasource_sql.views import CreateSQLDatabaseConnectionView, ListSQLDatabaseConnectionsView, \
    CreateSQLQueryView, UpdateSQLDatabaseConnectionView, DeleteSQLDatabaseConnectionView, UpdateSQLQueryView, \
    DeleteSQLQueryView, ListSQLQueriesView

app_name = "datasource_sql"

urlpatterns = [
    path("create/", CreateSQLDatabaseConnectionView.as_view(
        template_name="datasource_sql/connections/create_sql_datasources.html"
    ), name="create"),
    path("list/", ListSQLDatabaseConnectionsView.as_view(
        template_name="datasource_sql/connections/list_sql_datasources.html"
    ), name="list"),
    path("update/<int:pk>/", UpdateSQLDatabaseConnectionView.as_view(
        template_name="datasource_sql/connections/update_sql_datasources.html"
    ), name="update"),
    path("delete/<int:pk>/", DeleteSQLDatabaseConnectionView.as_view(), name="delete"),

    path("create_query/", CreateSQLQueryView.as_view(
        template_name="datasource_sql/queries/create_sql_query.html"
    ), name="create_query"),
    path("list_queries/", ListSQLQueriesView.as_view(
        template_name="datasource_sql/queries/list_sql_queries.html"
    ), name="list_queries"),
    path("update_query/<int:pk>/", UpdateSQLQueryView.as_view(
        template_name="datasource_sql/queries/update_sql_query.html"
    ), name="update_query"),
    path("delete_query/<int:pk>/", DeleteSQLQueryView.as_view(), name="delete_query"),
]
