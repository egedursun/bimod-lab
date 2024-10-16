#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-14 13:50:43
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-14 13:50:44
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

from apps.drafting.views import (DraftingView_DocumentDetail, DraftingView_DocumentDelete, DraftingView_DocumentCreate,
                                 DraftingView_DocumentList, DraftingView_FolderList, DraftingView_FolderCreate,
                                 DraftingView_FolderUpdate, DraftingView_FolderDelete, DraftingView_DocumentUpdate,
                                 DraftingView_SaveContent)

app_name = 'drafting'

urlpatterns = [
    path("folders/list/", DraftingView_FolderList.as_view(
        template_name="drafting/folder/drafting_folders_list.html"), name="folders_list"),
    path("folders/delete/<int:folder_id>/", DraftingView_FolderDelete.as_view(
        template_name="drafting/folder/drafting_folders_delete.html"), name="folders_delete"),
    path("folders/create/", DraftingView_FolderCreate.as_view(), name="folders_create"),
    path("folders/update/<int:folder_id>/", DraftingView_FolderUpdate.as_view(
        template_name="drafting/folder/drafting_folders_update.html"), name="folders_update"),

    path("documents/detail/<int:folder_id>/<int:document_id>/", DraftingView_DocumentDetail.as_view(
        template_name="drafting/document/drafting_documents_detail.html"), name="documents_detail"),
    path("documents/list/<int:folder_id>/", DraftingView_DocumentList.as_view(
        template_name="drafting/document/drafting_documents_list.html"), name="documents_list"),
    path("documents/delete/<int:folder_id>/<int:document_id>/", DraftingView_DocumentDelete.as_view(),
         name="documents_delete"),
    path("documents/create/<int:folder_id>/", DraftingView_DocumentCreate.as_view(), name="documents_create"),
    path("documents/update/<int:folder_id>/<int:document_id>/", DraftingView_DocumentUpdate.as_view(
        template_name="drafting/document/drafting_documents_update.html"
    ), name="documents_update"),
    path("documents/save/<int:folder_id>/<int:document_id>/", DraftingView_SaveContent.as_view(),
         name="documents_save"),
]
