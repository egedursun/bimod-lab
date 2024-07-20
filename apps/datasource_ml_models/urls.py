from django.urls import path

from .views import (DataSourceMLModelConnectionCreateView, DataSourceMLModelConnectionUpdateView,
                    DataSourceMLModelConnectionListView, DataSourceMLModelConnectionDeleteView,
                    DataSourceMLModelItemCreateView, DataSourceMLModelItemUpdateView,
                    DataSourceMLModelItemListView, DataSourceMLModelItemDeleteView)


app_name = 'datasource_ml_models'


urlpatterns = [
    path('create/', DataSourceMLModelConnectionCreateView.as_view(
        template_name='datasource_ml_models/base/create_datasource_ml_model.html'), name='create'),
    path('update/<int:pk>/', DataSourceMLModelConnectionUpdateView.as_view(
        template_name='datasource_ml_models/base/update_datasource_ml_model.html'), name='update'),
    path('list/', DataSourceMLModelConnectionListView.as_view(
        template_name='datasource_ml_models/base/list_datasource_ml_models.html'), name='list'),
    path('delete/<int:pk>/', DataSourceMLModelConnectionDeleteView.as_view(
        template_name='datasource_ml_models/base/confirm_delete_datasource_ml_model.html'), name='delete'),
    #################################################################################################################
    path('item/create/', DataSourceMLModelItemCreateView.as_view(
        template_name='datasource_ml_models/models/create_datasource_ml_model_item.html'), name='item_create'),
    path('item/update/<int:pk>/', DataSourceMLModelItemUpdateView.as_view(
        template_name='datasource_ml_models/models/update_datasource_ml_model_item.html'), name='item_update'),
    path('item/list/', DataSourceMLModelItemListView.as_view(
        template_name='datasource_ml_models/models/list_datasource_ml_model_items.html'), name='item_list'),
]
