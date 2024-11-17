#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-11-02 19:19:43
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 19:21:47
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

from apps.slider.views.google_apps_connection import SliderView_GoogleAppsConnectionList, \
    SliderView_GoogleAppsConnectionCreate, SliderView_GoogleAppsConnectionDelete, SliderView_GoogleAppsConnectionUpdate
from apps.slider.views.public import SliderView_PublicGenerateViaAICommand, SliderView_PublicGenerateViaNoSQLCommand, \
    SliderView_PublicGenerateViaSQLCommand, SliderView_PublicGenerateViaSSHCommand, \
    SliderView_PublicGenerateViaSelectCommand, SliderView_PublicGenerateViaVectCommand, \
    SliderView_PublicGenerateViaAutoCommand, SliderView_PublicGenerateViaImgCommand, \
    SliderView_PublicGenerateViaWebCommand, SliderView_PublicGenerateViaRepoCommand

app_name = 'slider'

urlpatterns = [
    # path("folders/list/", SliderView_FolderList
    # .as_view(
    #    template_name="slider/folder/slider_folders_list.html"), name="folders_list"),
    # path("folders/delete/<int:folder_id>/", SliderView_FolderDelete.as_view(
    #    template_name="slider/folder/slider_folders_delete.html"), name="folders_delete"),
    # path("folders/create/", SliderView_FolderCreate.as_view(), name="folders_create"),
    # path("folders/update/<int:folder_id>/", SliderView_FolderUpdate.as_view(
    #    template_name="slider/folder/slider_folders_update.html"), name="folders_update"),
    #
    # path("documents/detail/<int:folder_id>/<int:document_id>/", SliderView_DocumentDetail.as_view(
    #    template_name="slider/document/slider_documents_detail.html"), name="documents_detail"),
    # path("documents/list/<int:folder_id>/", SliderView_DocumentList.as_view(
    #    template_name="slider/document/slider_documents_list.html"), name="documents_list"),
    # path("documents/delete/<int:folder_id>/<int:document_id>/", SliderView_DocumentDelete.as_view(),
    #     name="documents_delete"),
    # path("documents/create/<int:folder_id>/", SliderView_DocumentCreate.as_view(), name="documents_create"),
    # path("documents/update/<int:folder_id>/<int:document_id>/", SliderView_DocumentUpdate.as_view(
    #    template_name="slider/document/slider_documents_update.html"
    # ), name="documents_update"),
    # path("documents/save/<int:folder_id>/<int:document_id>/", SliderView_SaveContent.as_view(),
    #     name="documents_save"),
    #
    # path("generate/commands/ai/", SliderView_GenerateViaAICommand.as_view(), name="generate_ai"),
    # path("generate/commands/nosql/", SliderView_GenerateViaNoSQLCommand.as_view(), name="generate_nosql"),
    # path("generate/commands/sql/", SliderView_GenerateViaSQLCommand.as_view(), name="generate_sql"),
    # path("generate/commands/ssh/", SliderView_GenerateViaSSHCommand.as_view(), name="generate_ssh"),
    # path("generate/commands/select/", SliderView_GenerateViaSelectCommand.as_view(), name="generate_select"),
    # path("generate/commands/vect/", SliderView_GenerateViaVectCommand.as_view(), name="generate_vect"),
    # path("generate/commands/auto/", SliderView_GenerateViaAutoCommand.as_view(), name="generate_auto"),
    # path("generate/commands/img/", SliderView_GenerateViaImgCommand.as_view(), name="generate_img"),
    # path("generate/commands/web/", SliderView_GenerateViaWebCommand.as_view(), name="generate_web"),
    # path("generate/commands/repo/", SliderView_GenerateViaRepoCommand.as_view(), name="generate_repo"),

    # Google Apps Connections
    path("google_apps/connections/list/", SliderView_GoogleAppsConnectionList.as_view(
        template_name="slider/google_apps_connection/manage_google_apps_connections.html"
    ), name="google_apps_connections_list"),
    path("google_apps/connections/create/", SliderView_GoogleAppsConnectionCreate.as_view(),
         name="google_apps_connections_create"),
    path("google_apps/connections/update/<int:pk>/", SliderView_GoogleAppsConnectionUpdate.as_view(),
         name="google_apps_connections_update"),
    path("google_apps/connections/delete/<int:pk>/", SliderView_GoogleAppsConnectionDelete.as_view(),
         name="google_apps_connections_delete"),

    # Public endpoints
    path("public/generate/commands/ai/", SliderView_PublicGenerateViaAICommand.as_view(), name="public_generate_ai"),
    path("public/generate/commands/nosql/", SliderView_PublicGenerateViaNoSQLCommand.as_view(),
         name="public_generate_nosql"),
    path("public/generate/commands/sql/", SliderView_PublicGenerateViaSQLCommand.as_view(),
         name="public_generate_sql"),
    path("public/generate/commands/ssh/", SliderView_PublicGenerateViaSSHCommand.as_view(),
         name="public_generate_ssh"),
    path("public/generate/commands/select/", SliderView_PublicGenerateViaSelectCommand.as_view(),
         name="public_generate_select"),
    path("public/generate/commands/vect/", SliderView_PublicGenerateViaVectCommand.as_view(),
         name="public_generate_vect"),
    path("public/generate/commands/auto/", SliderView_PublicGenerateViaAutoCommand.as_view(),
         name="public_generate_auto"),
    path("public/generate/commands/img/", SliderView_PublicGenerateViaImgCommand.as_view(),
         name="public_generate_img"),
    path("public/generate/commands/web/", SliderView_PublicGenerateViaWebCommand.as_view(),
         name="public_generate_web"),
    path("public/generate/commands/repo/", SliderView_PublicGenerateViaRepoCommand.as_view(),
         name="public_generate_repo"),
]
