#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-31 18:29:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 18:29:54
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

from apps.sheetos.views import (
    SheetosView_FolderList,
    SheetosView_FolderDelete,
    SheetosView_FolderCreate,
    SheetosView_FolderUpdate,
    SheetosView_DocumentDetail,
    SheetosView_DocumentList,
    SheetosView_DocumentDelete,
    SheetosView_DocumentCreate,
    SheetosView_DocumentUpdate,
    SheetosView_SaveContent,
    SheetosView_GenerateViaAICommand,
    SheetosView_GenerateViaNoSQLCommand,
    SheetosView_GenerateViaSQLCommand,
    SheetosView_GenerateViaSSHCommand,
    SheetosView_GenerateViaSelectCommand,
    SheetosView_GenerateViaAutoCommand,
    SheetosView_GenerateViaVectCommand,
    SheetosView_GenerateViaWebCommand,
    SheetosView_GenerateViaRepoCommand,
    SheetosView_GenerateViaSiteCommand,
    SheetosView_GoogleAppsConnectionList,
    SheetosView_GoogleAppsConnectionCreate,
    SheetosView_GoogleAppsConnectionUpdate,
    SheetosView_GoogleAppsConnectionDelete
)

from apps.sheetos.views.public import (
    SheetosView_PublicGenerateViaAICommand,
    SheetosView_PublicGenerateViaAutoCommand,
    SheetosView_PublicGenerateViaNoSQLCommand,
    SheetosView_PublicGenerateViaSQLCommand,
    SheetosView_PublicGenerateViaSSHCommand,
    SheetosView_PublicGenerateViaSelectCommand,
    SheetosView_PublicGenerateViaVectCommand,
    SheetosView_PublicGenerateViaWebCommand,
    SheetosView_PublicGenerateViaRepoCommand,
    SheetosView_PublicGenerateViaSiteCommand,
)

app_name = 'sheetos'

urlpatterns = [
    path(
        "folders/list/",
        SheetosView_FolderList.as_view(
            template_name="sheetos/folder/sheetos_folder_list.html"
        ),
        name="folders_list"
    ),

    path(
        "folders/delete/<int:folder_id>/",
        SheetosView_FolderDelete.as_view(
            template_name="sheetos/folder/sheetos_folder_delete.html"
        ),
        name="folders_delete"
    ),

    path(
        "folders/create/",
        SheetosView_FolderCreate.as_view(

        ),
        name="folders_create"
    ),

    path(
        "folders/update/<int:folder_id>/",
        SheetosView_FolderUpdate.as_view(
            template_name="sheetos/folder/sheetos_folder_update.html"
        ),
        name="folders_update"
    ),

    path(
        "documents/detail/<int:folder_id>/<int:document_id>/",
        SheetosView_DocumentDetail.as_view(
            template_name="sheetos/document/sheetos_document_detail.html"
        ),
        name="documents_detail"
    ),

    path(
        "documents/list/<int:folder_id>/",
        SheetosView_DocumentList.as_view(
            template_name="sheetos/document/sheetos_document_list.html"
        ),
        name="documents_list"
    ),

    path(
        "documents/delete/<int:folder_id>/<int:document_id>/",
        SheetosView_DocumentDelete.as_view(

        ),
        name="documents_delete"
    ),

    path(
        "documents/create/<int:folder_id>/",
        SheetosView_DocumentCreate.as_view(

        ),
        name="documents_create"
    ),

    path(
        "documents/update/<int:folder_id>/<int:document_id>/",
        SheetosView_DocumentUpdate.as_view(
            template_name="sheetos/document/sheetos_document_update.html"
        ),
        name="documents_update"
    ),

    path(
        "documents/save/<int:folder_id>/<int:document_id>/",
        SheetosView_SaveContent.as_view(

        ),
        name="documents_save"
    ),

    #####

    path(
        "generate/commands/ai/",
        SheetosView_GenerateViaAICommand.as_view(

        ),
        name="generate_ai"
    ),

    path(
        "generate/commands/nosql/",
        SheetosView_GenerateViaNoSQLCommand.as_view(

        ),
        name="generate_nosql"
    ),

    path(
        "generate/commands/sql/",
        SheetosView_GenerateViaSQLCommand.as_view(

        ),
        name="generate_sql"
    ),

    path(
        "generate/commands/ssh/",
        SheetosView_GenerateViaSSHCommand.as_view(

        ),
        name="generate_ssh"
    ),

    path(
        "generate/commands/select/",
        SheetosView_GenerateViaSelectCommand.as_view(

        ),
        name="generate_select"
    ),

    path(
        "generate/commands/vect/",
        SheetosView_GenerateViaVectCommand.as_view(

        ),
        name="generate_vect"
    ),

    path(
        "generate/commands/auto/",
        SheetosView_GenerateViaAutoCommand.as_view(

        ),
        name="generate_auto"
    ),

    path(
        "generate/commands/web/",
        SheetosView_GenerateViaWebCommand.as_view(

        ),
        name="generate_web"
    ),

    path(
        "generate/commands/repo/",
        SheetosView_GenerateViaRepoCommand.as_view(

        ),
        name="generate_repo"
    ),

    path(
        "generate/commands/site/",
        SheetosView_GenerateViaSiteCommand.as_view(

        ),
        name="generate_site"
    ),

    #####

    # Google Apps Connections

    path(
        "google_apps/connections/list/",
        SheetosView_GoogleAppsConnectionList.as_view(
            template_name="sheetos/google_apps_connection/manage_google_apps_connections.html"
        ),
        name="google_apps_connections_list"
    ),

    path(
        "google_apps/connections/create/",
        SheetosView_GoogleAppsConnectionCreate.as_view(

        ),
        name="google_apps_connections_create"
    ),

    path(
        "google_apps/connections/update/<int:pk>/",
        SheetosView_GoogleAppsConnectionUpdate.as_view(

        ),
        name="google_apps_connections_update"
    ),

    path(
        "google_apps/connections/delete/<int:pk>/",
        SheetosView_GoogleAppsConnectionDelete.as_view(

        ),
        name="google_apps_connections_delete"
    ),

    #####

    # Public endpoints
    path(
        "public/generate/commands/ai/",
        SheetosView_PublicGenerateViaAICommand.as_view(

        ),
        name="public_generate_ai"
    ),

    path(
        "public/generate/commands/nosql/",
        SheetosView_PublicGenerateViaNoSQLCommand.as_view(

        ),
        name="public_generate_nosql"
    ),

    path(
        "public/generate/commands/sql/",
        SheetosView_PublicGenerateViaSQLCommand.as_view(

        ),
        name="public_generate_sql"
    ),

    path(
        "public/generate/commands/ssh/",
        SheetosView_PublicGenerateViaSSHCommand.as_view(

        ),
        name="public_generate_ssh"
    ),

    path(
        "public/generate/commands/select/",
        SheetosView_PublicGenerateViaSelectCommand.as_view(

        ),
        name="public_generate_select"
    ),

    path(
        "public/generate/commands/vect/",
        SheetosView_PublicGenerateViaVectCommand.as_view(

        ),
        name="public_generate_vect"),

    path(
        "public/generate/commands/auto/",
        SheetosView_PublicGenerateViaAutoCommand.as_view(

        ),
        name="public_generate_auto"
    ),

    path(
        "public/generate/commands/web/",
        SheetosView_PublicGenerateViaWebCommand.as_view(

        ),
        name="public_generate_web"
    ),

    path(
        "public/generate/commands/repo/",
        SheetosView_PublicGenerateViaRepoCommand.as_view(

        ),
        name="public_generate_repo"
    ),

    path(
        "public/generate/commands/site/",
        SheetosView_PublicGenerateViaSiteCommand.as_view(

        ),
        name="public_generate_site"
    ),
]
