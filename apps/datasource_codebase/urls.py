#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:44
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
#  Last Modified: 2024-09-06 21:45:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:39:47
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path
from .views import (CodeBaseStorageCreateView, CodeBaseStorageUpdateView, CodeBaseStorageListView,
                    CodeBaseStorageDeleteView, AddRepositoryView, ListRepositoriesView, DeleteAllRepositoriesView)

app_name = 'datasource_codebase'

urlpatterns = [
    path('create/', CodeBaseStorageCreateView.as_view(
        template_name='datasource_codebase/storage/create_codebase_storage.html'
    ), name='create'),
    path('list/', CodeBaseStorageListView.as_view(
        template_name='datasource_codebase/storage/list_codebase_storages.html'
    ), name='list'),
    path('update/<int:pk>/', CodeBaseStorageUpdateView.as_view(
        template_name='datasource_codebase/storage/update_codebase_storage.html'
    ), name='update'),
    path('delete/<int:pk>/', CodeBaseStorageDeleteView.as_view(
        template_name='datasource_codebase/storage/confirm_delete_codebase_storage.html'
    ), name='delete'),

    ##############################

    path('create_repositories/', AddRepositoryView.as_view(
        template_name="datasource_codebase/repository/connect_codebase_repository.html"
    ), name="create_repositories"),
    path('list_repositories/', ListRepositoriesView.as_view(
        template_name="datasource_codebase/repository/list_codebase_repositories.html"
    ), name="list_repositories"),

    path('repositories/delete-selected/', ListRepositoriesView.as_view(), name='delete_selected_repositories'),
    path('repositories/delete-all/<int:kb_id>/', DeleteAllRepositoriesView.as_view(), name='delete_all_repositories'),
]
