#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-12-07 19:11:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 19:11:38
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

from apps.datasource_website.views import (
    DataSourceWebsiteView_StorageCreate,
    DataSourceWebsiteView_StorageList,
    DataSourceWebsiteView_StorageUpdate,
    DataSourceWebsiteView_StorageConfirmDelete,
    DataSourceWebsiteView_WebsiteItemCreate,
    DataSourceWebsiteView_WebsiteItemList,
    DataSourceWebsiteView_WebsiteItemRefresh,
    DataSourceWebsiteView_WebsiteItemConfirmDelete,
)

app_name = 'datasource_website'

urlpatterns = [
    path(
        'storage/create/',
        DataSourceWebsiteView_StorageCreate.as_view(
            template_name='datasource_website/connection/create_website_storage_connection.html'
        ),
        name='storage_create'
    ),

    path(
        'storage/list/',
        DataSourceWebsiteView_StorageList.as_view(
            template_name='datasource_website/connection/list_website_storage_connections.html'
        ),
        name='storage_list'
    ),

    path(
        'storage/update/<int:pk>/',
        DataSourceWebsiteView_StorageUpdate.as_view(
            template_name='datasource_website/connection/update_website_storage_connection.html'
        ),
        name='storage_update'
    ),

    path(
        'storage/delete/<int:pk>/',
        DataSourceWebsiteView_StorageConfirmDelete.as_view(
            template_name='datasource_website/connection/confirm_delete_website_storage_connection.html'
        ),
        name='storage_delete'
    ),

    ######

    path(
        'website_item/list/',
        DataSourceWebsiteView_WebsiteItemList.as_view(
            template_name='datasource_website/website_item/list_create_website_item.html'
        ),
        name='website_item_list'
    ),

    path(
        'website_item/delete/<int:pk>/',
        DataSourceWebsiteView_WebsiteItemConfirmDelete.as_view(
            template_name='datasource_website/website_item/confirm_delete_website_item.html'
        ),
        name='website_item_delete'
    ),

    path(
        'website_item/create/',
        DataSourceWebsiteView_WebsiteItemCreate.as_view(

        ),
        name='website_item_create'
    ),

    path(
        'website_item/refresh/<int:pk>/',
        DataSourceWebsiteView_WebsiteItemRefresh.as_view(

        ),
        name='website_item_refresh'
    ),
]
