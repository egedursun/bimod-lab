#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.urls import path

from apps.datasource_knowledge_base.views import DocumentKnowledgeBaseCreateView, DocumentKnowledgeBaseListView, \
    DocumentKnowledgeBaseUpdateView, DocumentKnowledgeBaseDeleteView, AddDocumentView, ListDocumentsView, \
    DeleteAllDocumentsView

app_name = "datasource_knowledge_base"

urlpatterns = [
    path("create/", DocumentKnowledgeBaseCreateView.as_view(
        template_name="datasource_knowledge_base/base/create_knowledge_base.html"
    ), name="create"),
    path("list/", DocumentKnowledgeBaseListView.as_view(
        template_name="datasource_knowledge_base/base/list_knowledge_bases.html"
    ), name="list"),
    path("update/<int:pk>/", DocumentKnowledgeBaseUpdateView.as_view(
        template_name="datasource_knowledge_base/base/update_knowledge_base.html"
    ), name="update"),
    path("delete/<int:pk>/", DocumentKnowledgeBaseDeleteView.as_view(
        template_name="datasource_knowledge_base/base/confirm_delete_knowledge_base.html"
    ), name="delete"),

    path('create_documents/', AddDocumentView.as_view(
        template_name="datasource_knowledge_base/document/add_document.html"
    ), name="create_documents"),
    path('list_documents/', ListDocumentsView.as_view(
        template_name="datasource_knowledge_base/document/list_documents.html"
    ), name="list_documents"),

    path('documents/delete-selected/', ListDocumentsView.as_view(), name='delete_selected_documents'),
    path('documents/delete-all/<int:kb_id>/', DeleteAllDocumentsView.as_view(), name='delete_all_documents'),
]
