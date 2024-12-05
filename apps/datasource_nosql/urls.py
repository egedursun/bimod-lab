#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-10 16:16:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-10 16:16:14
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.urls import path

from apps.datasource_nosql.views.nosql_database import (
    NoSQLDatabaseView_ManagerCreate,
    NoSQLDatabaseView_ManagerList,
    NoSQLDatabaseView_ManagerUpdate,
    NoSQLDatabaseView_ManagerDelete,
    NoSQLDatabaseView_ManagerRefreshSchema,
)

from apps.datasource_nosql.views.nosql_query import (
    NoSQLDatabaseView_QueryCreate,
    NoSQLDatabaseView_QueryList,
    NoSQLDatabaseView_QueryUpdate,
    NoSQLDatabaseView_QueryDelete
)

app_name = "datasource_nosql"

urlpatterns = [
    path(
        "create/",
        NoSQLDatabaseView_ManagerCreate.as_view(
            template_name="datasource_nosql/connections/create_nosql_datasources.html"
        ),
        name="create"
    ),

    path(
        "list/",
        NoSQLDatabaseView_ManagerList.as_view(
            template_name="datasource_nosql/connections/list_nosql_datasources.html"
        ),
        name="list"
    ),

    path(
        "update/<int:pk>/",
        NoSQLDatabaseView_ManagerUpdate.as_view(
            template_name="datasource_nosql/connections/update_nosql_datasources.html"
        ),
        name="update"
    ),

    path(
        "delete/<int:pk>/",
        NoSQLDatabaseView_ManagerDelete.as_view(

        ),
        name="delete"
    ),

    path(
        'refresh_schema/<int:pk>/',
        NoSQLDatabaseView_ManagerRefreshSchema.as_view(

        ),
        name='refresh_schema'
    ),

    path(
        "create_query/",
        NoSQLDatabaseView_QueryCreate.as_view(
            template_name="datasource_nosql/queries/create_nosql_query.html"
        ),
        name="create_query"
    ),

    path(
        "list_queries/",
        NoSQLDatabaseView_QueryList.as_view(
            template_name="datasource_nosql/queries/list_nosql_queries.html"
        ),
        name="list_queries"
    ),

    path(
        "update_query/<int:pk>/",
        NoSQLDatabaseView_QueryUpdate.as_view(
            template_name="datasource_nosql/queries/update_nosql_query.html"
        ),
        name="update_query"
    ),

    path(
        "delete_query/<int:pk>/",
        NoSQLDatabaseView_QueryDelete.as_view(

        ),
        name="delete_query"
    ),
]
