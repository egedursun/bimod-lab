#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:47
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

from apps.datasource_knowledge_base.views import VectorStoreView_Create, VectorStoreView_List, \
    VectorStoreView_Update, VectorStoreView_Delete, DocumentView_Create, DocumentView_List, \
    DocumentView_DeleteAll

app_name = "datasource_knowledge_base"

urlpatterns = [
    path(
        "create/",
        VectorStoreView_Create.as_view(
            template_name="datasource_knowledge_base/base/create_knowledge_base.html"
        ),
        name="create"
    ),

    path(
        "list/",
        VectorStoreView_List.as_view(
            template_name="datasource_knowledge_base/base/list_knowledge_bases.html"
        ),
        name="list"
    ),

    path(
        "update/<int:pk>/",
        VectorStoreView_Update.as_view(
            template_name="datasource_knowledge_base/base/update_knowledge_base.html"
        ),
        name="update"
    ),

    path(
        "delete/<int:pk>/",
        VectorStoreView_Delete.as_view(
            template_name="datasource_knowledge_base/base/confirm_delete_knowledge_base.html"
        ),
        name="delete"
    ),

    path(
        'create_documents/',
        DocumentView_Create.as_view(
            template_name="datasource_knowledge_base/document/add_document.html"
        ),
        name="create_documents"
    ),

    path(
        'list_documents/',
        DocumentView_List.as_view(
            template_name="datasource_knowledge_base/document/list_documents.html"
        ),
        name="list_documents"
    ),

    path(
        'documents/delete-selected/',
        DocumentView_List.as_view(

        ),
        name='delete_selected_documents'
    ),

    path(
        'documents/delete-all/<int:kb_id>/',
        DocumentView_DeleteAll.as_view(

        ),
        name='delete_all_documents'
    ),
]
