#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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
from .views import (CodeBaseView_StorageCreate, CodeBaseView_StorageUpdate, CodeBaseView_StorageList,
                    CodeBaseView_StorageDelete, CodeBaseView_RepositoryCreate, CodeBaseView_RepositoryList, CodeBaseView_RepositoryDeleteAll)

app_name = 'datasource_codebase'

urlpatterns = [
    path('create/', CodeBaseView_StorageCreate.as_view(
        template_name='datasource_codebase/storage/create_codebase_storage.html'
    ), name='create'),
    path('list/', CodeBaseView_StorageList.as_view(
        template_name='datasource_codebase/storage/list_codebase_storages.html'
    ), name='list'),
    path('update/<int:pk>/', CodeBaseView_StorageUpdate.as_view(
        template_name='datasource_codebase/storage/update_codebase_storage.html'
    ), name='update'),
    path('delete/<int:pk>/', CodeBaseView_StorageDelete.as_view(
        template_name='datasource_codebase/storage/confirm_delete_codebase_storage.html'
    ), name='delete'),
    path('create_repositories/', CodeBaseView_RepositoryCreate.as_view(
        template_name="datasource_codebase/repository/connect_codebase_repository.html"
    ), name="create_repositories"),
    path('list_repositories/', CodeBaseView_RepositoryList.as_view(
        template_name="datasource_codebase/repository/list_codebase_repositories.html"
    ), name="list_repositories"),
    path('repositories/delete-selected/', CodeBaseView_RepositoryList.as_view(), name='delete_selected_repositories'),
    path('repositories/delete-all/<int:kb_id>/', CodeBaseView_RepositoryDeleteAll.as_view(), name='delete_all_repositories'),
]
