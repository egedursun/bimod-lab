#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:48
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

from apps.datasource_media_storages.views import MediaView_ManagerCreate, \
    MediaView_ManagerList, MediaView_ManagerUpdate, \
    MediaView_ManagerDelete, MediaView_ItemCreate, \
    MediaView_ItemList, MediaView_ItemDeleteAll, \
    MediaView_ItemUpdate, MediaView_ItemAIDescription, \
    MediaView_ItemHTTPRetrieval, MediaView_Generated

app_name = "datasource_media_storages"

urlpatterns = [
    path('create/', MediaView_ManagerCreate.as_view(
        template_name="datasource_media_storages/storage/create_datasource_media_storage.html"), name="create"),
    path('list/', MediaView_ManagerList.as_view(
        template_name="datasource_media_storages/storage/list_datasource_media_storages.html"), name="list"),
    path('update/<int:pk>/', MediaView_ManagerUpdate.as_view(
        template_name="datasource_media_storages/storage/update_datasource_media_storage.html"), name="update"),
    path('delete/<int:pk>/', MediaView_ManagerDelete.as_view(
        template_name="datasource_media_storages/storage/confirm_delete_datasource_media_storage.html"
    ), name="delete"),
    path('create_item/', MediaView_ItemCreate.as_view(
        template_name="datasource_media_storages/media/add_media.html"), name="create_item"),
    path('list_items/', MediaView_ItemList.as_view(
        template_name="datasource_media_storages/media/list_medias.html"), name="list_items"),
    path('item/detail/<int:pk>/', MediaView_ItemUpdate.as_view(
        template_name="datasource_media_storages/media/detail_media.html"), name='item_detail'),
    path('items/delete-selected/', MediaView_ItemList.as_view(), name='delete_selected_items'),
    path('items/delete-all/<int:id>/', MediaView_ItemDeleteAll.as_view(), name='delete_all_items'),
    path('items/generate_description/<int:pk>/', MediaView_ItemAIDescription.as_view(
        template_name="datasource_media_storages/media/detail_media.html"), name='generate_description'),
    path('items/fetch_file_from_url/', MediaView_ItemHTTPRetrieval.as_view(),
         name='fetch_file_from_url'),
    path('items/list_generated/', MediaView_Generated.as_view(
        template_name="datasource_media_storages/generated/list_generated_media.html"), name='list_generated_items'),
]
