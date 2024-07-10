from django.urls import path

from apps.datasource_sql.views import CreateSQLDatabaseConnectionView, ListSQLDatabaseConnectionsView, \
    CreateSQLQueryView, UpdateSQLDatabaseConnectionView, DeleteSQLDatabaseConnectionView, UpdateSQLQueryView, \
    DeleteSQLQueryView, ListSQLQueriesView

app_name = "datasource_sql"


urlpatterns = [
    path("create/", CreateSQLDatabaseConnectionView.as_view(
        template_name="datasource_sql/create_sql_datasources.html"
    ), name="create"),
    path("list/", ListSQLDatabaseConnectionsView.as_view(
        template_name="datasource_sql/list_sql_datasources.html"
    ), name="list"),
    path("update/<int:pk>/", UpdateSQLDatabaseConnectionView.as_view(
        template_name="datasource_sql/update_sql_datasources.html"
    ), name="update"),
    path("delete/<int:pk>/", DeleteSQLDatabaseConnectionView.as_view(), name="delete"),

    ##################################################

    path("create_query/", CreateSQLQueryView.as_view(
        template_name="datasource_sql/create_sql_query.html"
    ), name="create_query"),
    path("list_queries/", ListSQLQueriesView.as_view(
        template_name="datasource_sql/list_sql_queries.html"
    ), name="list_queries"),
    path("update_query/<int:pk>/", UpdateSQLQueryView.as_view(
        template_name="datasource_sql/update_sql_query.html"
    ), name="update_query"),
    path("delete_query/<int:pk>/", DeleteSQLQueryView.as_view(), name="delete_query"),
]
