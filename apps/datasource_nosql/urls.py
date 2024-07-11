from django.urls import path

from apps.datasource_nosql.views import CreateNoSQLDataSourcesView, UpdateNoSQLDataSourceView, \
    DeleteNoSQLDataSourceView, ListNoSQLDataSourcesView, CreateNoSQLQueryView, UpdateNoSQLQueryView, \
    DeleteNoSQLQueryView, ListNoSQLQueriesView

app_name = 'datasource_nosql'


urlpatterns = [
    path('create/', CreateNoSQLDataSourcesView.as_view(
        template_name="datasource_nosql/create_nosql_datasources.html"
    ), name='create'),
    path('update/<int:pk>/', UpdateNoSQLDataSourceView.as_view(
        template_name="datasource_nosql/update_nosql_datasource.html"
    ), name='update'),
    path('delete/<int:pk>/', DeleteNoSQLDataSourceView.as_view(), name='delete'),
    path('list/', ListNoSQLDataSourcesView.as_view(
        template_name="datasource_nosql/list_nosql_datasources.html"
    ), name='list'),
    ####################################################################################################
    path('create_query/', CreateNoSQLQueryView.as_view(
        template_name="datasource_nosql/create_nosql_query.html"
    ), name='create_query'),
    path('update_query/<int:pk>/', UpdateNoSQLQueryView.as_view(
        template_name="datasource_nosql/update_nosql_query.html"
    ), name='update_query'),
    path('delete_query/<int:pk>/', DeleteNoSQLQueryView.as_view(), name='delete_query'),
    path('list_queries/', ListNoSQLQueriesView.as_view(
        template_name="datasource_nosql/list_nosql_queries.html"
    ), name='list_queries'),
]
