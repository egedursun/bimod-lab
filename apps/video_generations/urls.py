#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-10-01 22:54:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:43
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
#  Last Modified: 2024-10-01 17:02:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 17:32:08
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#
from django.urls import path

from apps.video_generations.views import (CreateVideoGeneratorConnectionView, UpdateVideoGeneratorConnectionView,
                                          ListVideoGeneratorConnectionsView, DeleteVideoGeneratorConnectionView)

app_name = 'video_generations'

urlpatterns = [
    path('create/', CreateVideoGeneratorConnectionView.as_view(
        template_name='video_generations/connection/create_video_generator_connection.html'), name='create'),
    path('update/<int:pk>/', UpdateVideoGeneratorConnectionView.as_view(
        template_name='video_generations/connection/update_video_generator_connection.html'), name='update'),
    path('list/', ListVideoGeneratorConnectionsView.as_view(
        template_name='video_generations/connection/list_video_generator_connections.html'), name='list'),
    path('delete/<int:pk>/', DeleteVideoGeneratorConnectionView.as_view(
        template_name='video_generations/connection/confirm_delete_video_generator_connection.html'), name='delete'),
]
