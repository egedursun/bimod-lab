#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-08-30 13:22:33
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:54:09
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from .views import (FineTunedModelConnectionRemoveView,
                    FineTunedModelConnectionAddView, FineTunedModelConnectionsListView)

app_name = 'finetuning'

urlpatterns = [
    ############################
    path('list/', FineTunedModelConnectionsListView.as_view(
        template_name='finetuning/list_finetuned_connections.html'
    ), name='list'),
    path('add/', FineTunedModelConnectionAddView.as_view(
        template_name='finetuning/list_finetuned_connections.html'), name='add'),
    path('remove/<int:pk>/', FineTunedModelConnectionRemoveView.as_view(
        template_name='finetuning/list_finetuned_connections.html'
    ), name='remove'),
    ############################
]
