#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-09-27 12:19:22
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:47:29
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.datasource_media_storages.views import DataSourceMediaStorageConnectionCreateView, \
    DataSourceListMediaStorageConnectionsView, DataSourceMediaStorageConnectionUpdateView, \
    DataSourceMediaStorageConnectionDeleteView, DataSourceMediaStorageItemCreateView, \
    DataSourceMediaStorageItemListView, DataSourceMediaStorageAllItemsDeleteView, \
    DataSourceMediaStorageItemDetailAndUpdateView, DataSourceMediaStorageItemGenerateDescription, \
    DataSourceMediaStorageItemFetchFileFromUrl, DataSourceMediaStorageGeneratedItemsListView

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
    path('items/fetch_file_from_url/', DataSourceMediaStorageItemFetchFileFromUrl.as_view(),
         name='fetch_file_from_url'),

    path('items/list_generated/', DataSourceMediaStorageGeneratedItemsListView.as_view(
        template_name="datasource_media_storages/generated/list_generated_media.html"
    ), name='list_generated_items'),

    #####
]
