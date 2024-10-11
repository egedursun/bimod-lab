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
from . import views

app_name = 'datasource_file_systems'

urlpatterns = [
    path('create/', views.FileSystemView_Create.as_view(
        template_name='datasource_file_systems/create_datasource_file_system.html'), name='create'),
    path('update/<int:pk>/', views.FileSystemView_Update.as_view(
        template_name='datasource_file_systems/update_datasource_file_system.html'), name='update'),
    path('list/', views.FileSystemView_List.as_view(
        template_name='datasource_file_systems/list_datasource_file_systems.html'), name='list'),
    path('delete/<int:pk>/', views.FileSystemView_Delete.as_view(), name='delete'),
]
