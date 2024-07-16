from django.urls import path
from . import views

app_name = 'datasource_file_systems'


urlpatterns = [
    path('create/', views.DataSourceFileSystemListCreateView.as_view(
        template_name='datasource_file_systems/create_datasource_file_system.html'
    ), name='create'),
    path('update/<int:pk>/', views.DataSourceFileSystemUpdateView.as_view(
        template_name='datasource_file_systems/update_datasource_file_system.html'
    ), name='update'),
    path('list/', views.DataSourceFileSystemsListView.as_view(
        template_name='datasource_file_systems/list_datasource_file_systems.html'
    ), name='list'),
    path('delete/<int:pk>/', views.DataSourceFileSystemDeleteView.as_view(), name='delete'),
]
