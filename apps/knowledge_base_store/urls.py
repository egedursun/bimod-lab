#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-11-06 23:24:11
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-06 23:24:13
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

from apps.knowledge_base_store.views import (
    KnowledgeBaseStoreView_StoreKnowledgeBaseList,
    KnowledgeBaseStoreView_IntegrateKnowledgeBase
)

app_name = 'knowledge_base_store'

urlpatterns = [
    path(
        'list/',
        KnowledgeBaseStoreView_StoreKnowledgeBaseList.as_view(
            template_name='knowledge_base_store/store_knowledge_bases_list.html'
        ),
        name='list'
    ),

    path(
        "integrate/<int:pk>/",
        KnowledgeBaseStoreView_IntegrateKnowledgeBase.as_view(

        ),
        name="integrate"
    ),
]
