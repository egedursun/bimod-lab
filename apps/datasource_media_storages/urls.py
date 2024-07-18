from django.urls import path

from apps.datasource_media_storages.views import DataSourceMediaStorageConnectionCreateView, \
    DataSourceListMediaStorageConnectionsView, DataSourceMediaStorageConnectionUpdateView, \
    DataSourceMediaStorageConnectionDeleteView, DataSourceMediaStorageItemCreateView, \
    DataSourceMediaStorageItemListView, DataSourceMediaStorageAllItemsDeleteView, \
    DataSourceMediaStorageItemDetailAndUpdateView, DataSourceMediaStorageItemGenerateDescription

app_name = "datasource_media_storages"


urlpatterns = [
    path('create/', DataSourceMediaStorageConnectionCreateView.as_view(
        template_name="datasource_media_storages/storage/create_datasource_media_storage.html"
    ), name="create"),
    path('list/', DataSourceListMediaStorageConnectionsView.as_view(
        template_name="datasource_media_storages/storage/list_datasource_media_storages.html"
    ), name="list"),
    path('update/<int:pk>/', DataSourceMediaStorageConnectionUpdateView.as_view(
        template_name="datasource_media_storages/storage/update_datasource_media_storage.html"
    ), name="update"),
    path('delete/<int:pk>/', DataSourceMediaStorageConnectionDeleteView.as_view(
        template_name="datasource_media_storages/storage/confirm_delete_datasource_media_storage.html"
    ), name="delete"),
    path('create_item/', DataSourceMediaStorageItemCreateView.as_view(
        template_name="datasource_media_storages/media/add_media.html"
    ), name="create_item"),
    path('list_items/', DataSourceMediaStorageItemListView.as_view(
        template_name="datasource_media_storages/media/list_medias.html"
    ), name="list_items"),
    path('item/detail/<int:pk>/', DataSourceMediaStorageItemDetailAndUpdateView.as_view(
        template_name="datasource_media_storages/media/detail_media.html"
    ), name='item_detail'),
    path('items/delete-selected/', DataSourceMediaStorageItemListView.as_view(), name='delete_selected_items'),
    path('items/delete-all/<int:id>/', DataSourceMediaStorageAllItemsDeleteView.as_view(), name='delete_all_items'),
    path('items/generate_description/<int:pk>/', DataSourceMediaStorageItemGenerateDescription.as_view(
        template_name="datasource_media_storages/media/detail_media.html"
    ), name='generate_description'),
]
