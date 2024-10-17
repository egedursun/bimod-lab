#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
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

from .views import (FineTuningView_Delete,
                    FineTuningView_Add, FineTuningView_List)

app_name = 'finetuning'

urlpatterns = [
    path('list/', FineTuningView_List.as_view(
        template_name='finetuning/list_finetuned_connections.html'), name='list'),
    path('add/', FineTuningView_Add.as_view(
        template_name='finetuning/list_finetuned_connections.html'), name='add'),
    path('remove/<int:pk>/', FineTuningView_Delete.as_view(
        template_name='finetuning/list_finetuned_connections.html'), name='remove'),
]
