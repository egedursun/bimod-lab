#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.urls import path

from apps.video_generations.views import (VideoGeneratorView_Create, VideoGeneratorView_Update,
                                          VideoGeneratorView_Connections, VideoGeneratorView_ConfirmDelete)

app_name = 'video_generations'

urlpatterns = [
    path('create/', VideoGeneratorView_Create.as_view(
        template_name='video_generations/connection/create_video_generator_connection.html'), name='create'),
    path('update/<int:pk>/', VideoGeneratorView_Update.as_view(
        template_name='video_generations/connection/update_video_generator_connection.html'), name='update'),
    path('list/', VideoGeneratorView_Connections.as_view(
        template_name='video_generations/connection/list_video_generator_connections.html'), name='list'),
    path('delete/<int:pk>/', VideoGeneratorView_ConfirmDelete.as_view(
        template_name='video_generations/connection/confirm_delete_video_generator_connection.html'), name='delete'),
]
