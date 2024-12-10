#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.urls import path

from apps.drafting.views import (
    DraftingView_DocumentDetail,
    DraftingView_DocumentDelete,
    DraftingView_DocumentCreate,
    DraftingView_DocumentList,
    DraftingView_FolderList,
    DraftingView_FolderCreate,
    DraftingView_FolderUpdate,
    DraftingView_FolderDelete,
    DraftingView_DocumentUpdate,
    DraftingView_SaveContent,
    DraftingView_GenerateViaAICommand,
    DraftingView_GenerateViaNoSQLCommand,
    DraftingView_GenerateViaSQLCommand,
    DraftingView_GenerateViaSSHCommand,
    DraftingView_GenerateViaSelectCommand,
    DraftingView_GenerateViaVectCommand,
    DraftingView_GenerateViaAutoCommand,
    DraftingView_GenerateViaImgCommand,
    DraftingView_GenerateViaWebCommand,
    DraftingView_PublicGenerateViaNoSQLCommand,
    DraftingView_PublicGenerateViaAICommand,
    DraftingView_PublicGenerateViaSQLCommand,
    DraftingView_PublicGenerateViaSelectCommand,
    DraftingView_PublicGenerateViaVectCommand,
    DraftingView_PublicGenerateViaWebCommand,
    DraftingView_PublicGenerateViaAutoCommand,
    DraftingView_PublicGenerateViaImgCommand,
    DraftingView_PublicGenerateViaRepoCommand,
    DraftingView_PublicGenerateViaSSHCommand,
    DraftingView_GoogleAppsConnectionCreate,
    DraftingView_GoogleAppsConnectionUpdate,
    DraftingView_GoogleAppsConnectionDelete,
    DraftingView_GoogleAppsConnectionList,
    DraftingView_GenerateViaRepoCommand,
    DraftingView_GenerateViaSiteCommand,
    DraftingView_PublicGenerateViaSiteCommand,
)

app_name = 'drafting'

urlpatterns = [
    path(
        "folders/list/",
        DraftingView_FolderList.as_view(
            template_name="drafting/folder/drafting_folders_list.html"
        ),
        name="folders_list"
    ),

    path(
        "folders/delete/<int:folder_id>/",
        DraftingView_FolderDelete.as_view(
            template_name="drafting/folder/drafting_folders_delete.html"
        ),
        name="folders_delete"
    ),

    path(
        "folders/create/",
        DraftingView_FolderCreate.as_view(

        ),
        name="folders_create"
    ),

    path(
        "folders/update/<int:folder_id>/",
        DraftingView_FolderUpdate.as_view(
            template_name="drafting/folder/drafting_folders_update.html"
        ),
        name="folders_update"
    ),

    path(
        "documents/detail/<int:folder_id>/<int:document_id>/",
        DraftingView_DocumentDetail.as_view(
            template_name="drafting/document/drafting_documents_detail.html"
        ),
        name="documents_detail"
    ),

    path(
        "documents/list/<int:folder_id>/",
        DraftingView_DocumentList.as_view(
            template_name="drafting/document/drafting_documents_list.html"
        ),
        name="documents_list"
    ),

    path(
        "documents/delete/<int:folder_id>/<int:document_id>/",
        DraftingView_DocumentDelete.as_view(

        ),
        name="documents_delete"
    ),

    path(
        "documents/create/<int:folder_id>/",
        DraftingView_DocumentCreate.as_view(

        ),
        name="documents_create"
    ),

    path(
        "documents/update/<int:folder_id>/<int:document_id>/",
        DraftingView_DocumentUpdate.as_view(
            template_name="drafting/document/drafting_documents_update.html"
        ),
        name="documents_update"
    ),

    path(
        "documents/save/<int:folder_id>/<int:document_id>/",
        DraftingView_SaveContent.as_view(

        ),
        name="documents_save"
    ),

    #####

    path(
        "generate/commands/ai/",
        DraftingView_GenerateViaAICommand.as_view(

        ),
        name="generate_ai"
    ),

    path(
        "generate/commands/nosql/",
        DraftingView_GenerateViaNoSQLCommand.as_view(

        ),
        name="generate_nosql"
    ),

    path(
        "generate/commands/sql/",
        DraftingView_GenerateViaSQLCommand.as_view(

        ),
        name="generate_sql"
    ),

    path(
        "generate/commands/ssh/",
        DraftingView_GenerateViaSSHCommand.as_view(

        ),
        name="generate_ssh"
    ),

    path(
        "generate/commands/select/",
        DraftingView_GenerateViaSelectCommand.as_view(

        ),
        name="generate_select"
    ),

    path(
        "generate/commands/vect/",
        DraftingView_GenerateViaVectCommand.as_view(

        ),
        name="generate_vect"
    ),

    path(
        "generate/commands/auto/",
        DraftingView_GenerateViaAutoCommand.as_view(

        ),
        name="generate_auto"
    ),

    path(
        "generate/commands/img/",
        DraftingView_GenerateViaImgCommand.as_view(

        ),
        name="generate_img"
    ),

    path(
        "generate/commands/web/",
        DraftingView_GenerateViaWebCommand.as_view(

        ),
        name="generate_web"
    ),

    path(
        "generate/commands/repo/",
        DraftingView_GenerateViaRepoCommand.as_view(

        ),
        name="generate_repo"
    ),

    path(
        "generate/commands/site/",
        DraftingView_GenerateViaSiteCommand.as_view(

        ),
        name="generate_site"
    ),

    #####

    # Google Apps Connections

    path(
        "google_apps/connections/list/",
        DraftingView_GoogleAppsConnectionList.as_view(
            template_name="drafting/google_apps_connection/manage_google_apps_connections.html"
        ),
        name="google_apps_connections_list"
    ),

    path(
        "google_apps/connections/create/",
        DraftingView_GoogleAppsConnectionCreate.as_view(

        ),
        name="google_apps_connections_create"
    ),

    path(
        "google_apps/connections/update/<int:pk>/",
        DraftingView_GoogleAppsConnectionUpdate.as_view(

        ),
        name="google_apps_connections_update"
    ),

    path(
        "google_apps/connections/delete/<int:pk>/",
        DraftingView_GoogleAppsConnectionDelete.as_view(

        ),
        name="google_apps_connections_delete"
    ),

    #####

    # Public endpoints
    path(
        "public/generate/commands/ai/",
        DraftingView_PublicGenerateViaAICommand.as_view(

        ), name="public_generate_ai"
    ),

    path(
        "public/generate/commands/nosql/",
        DraftingView_PublicGenerateViaNoSQLCommand.as_view(

        ),
        name="public_generate_nosql"
    ),

    path(
        "public/generate/commands/sql/",
        DraftingView_PublicGenerateViaSQLCommand.as_view(

        ),
        name="public_generate_sql"
    ),

    path(
        "public/generate/commands/ssh/",
        DraftingView_PublicGenerateViaSSHCommand.as_view(

        ),
        name="public_generate_ssh"
    ),

    path(
        "public/generate/commands/select/",
        DraftingView_PublicGenerateViaSelectCommand.as_view(

        ),
        name="public_generate_select"
    ),

    path(
        "public/generate/commands/vect/",
        DraftingView_PublicGenerateViaVectCommand.as_view(

        ),
        name="public_generate_vect"
    ),

    path(
        "public/generate/commands/auto/",
        DraftingView_PublicGenerateViaAutoCommand.as_view(

        ),
        name="public_generate_auto"
    ),

    path(
        "public/generate/commands/img/",
        DraftingView_PublicGenerateViaImgCommand.as_view(

        ),
        name="public_generate_img"
    ),

    path(
        "public/generate/commands/web/",
        DraftingView_PublicGenerateViaWebCommand.as_view(

        ),
        name="public_generate_web"
    ),

    path(
        "public/generate/commands/repo/",
        DraftingView_PublicGenerateViaRepoCommand.as_view(

        ),
        name="public_generate_repo"
    ),

    path(
        "public/generate/commands/site/",
        DraftingView_PublicGenerateViaSiteCommand.as_view(

        ),
        name="public_generate_site"
    ),
]
