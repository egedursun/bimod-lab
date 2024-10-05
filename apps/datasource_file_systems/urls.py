#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:45
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
#  Last Modified: 2024-08-02 10:52:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:41:17
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

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
