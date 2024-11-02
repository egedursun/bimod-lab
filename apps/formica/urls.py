#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-11-02 12:45:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 12:45:28
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

from apps.formica.views import FormicaView_GoogleAppsConnectionList, FormicaView_GoogleAppsConnectionCreate, \
    FormicaView_GoogleAppsConnectionUpdate, FormicaView_GoogleAppsConnectionDelete, \
    FormicaView_PublicGenerateViaAICommand, FormicaView_PublicGenerateViaNoSQLCommand, \
    FormicaView_PublicGenerateViaSQLCommand, FormicaView_PublicGenerateViaSSHCommand, \
    FormicaView_PublicGenerateViaSelectCommand, FormicaView_PublicGenerateViaVectCommand, \
    FormicaView_PublicGenerateViaAutoCommand, FormicaView_PublicGenerateViaImgCommand, \
    FormicaView_PublicGenerateViaWebCommand, FormicaView_PublicGenerateViaRepoCommand

app_name = 'formica'

urlpatterns = [
    # Google Apps Connections
    path("google_apps/connections/list/", FormicaView_GoogleAppsConnectionList.as_view(
        template_name="formica/manage_google_apps_connections.html"
    ), name="google_apps_connections_list"),
    path("google_apps/connections/create/", FormicaView_GoogleAppsConnectionCreate.as_view(),
         name="google_apps_connections_create"),
    path("google_apps/connections/update/<int:pk>/", FormicaView_GoogleAppsConnectionUpdate.as_view(),
         name="google_apps_connections_update"),
    path("google_apps/connections/delete/<int:pk>/", FormicaView_GoogleAppsConnectionDelete.as_view(),
         name="google_apps_connections_delete"),

    # Public endpoints
    path("public/generate/commands/ai/", FormicaView_PublicGenerateViaAICommand.as_view(), name="public_generate_ai"),
    path("public/generate/commands/nosql/", FormicaView_PublicGenerateViaNoSQLCommand.as_view(),
         name="public_generate_nosql"),
    path("public/generate/commands/sql/", FormicaView_PublicGenerateViaSQLCommand.as_view(),
         name="public_generate_sql"),
    path("public/generate/commands/ssh/", FormicaView_PublicGenerateViaSSHCommand.as_view(),
         name="public_generate_ssh"),
    path("public/generate/commands/select/", FormicaView_PublicGenerateViaSelectCommand.as_view(),
         name="public_generate_select"),
    path("public/generate/commands/vect/", FormicaView_PublicGenerateViaVectCommand.as_view(),
         name="public_generate_vect"),
    path("public/generate/commands/auto/", FormicaView_PublicGenerateViaAutoCommand.as_view(),
         name="public_generate_auto"),
    path("public/generate/commands/img/", FormicaView_PublicGenerateViaImgCommand.as_view(),
         name="public_generate_img"),
    path("public/generate/commands/web/", FormicaView_PublicGenerateViaWebCommand.as_view(),
         name="public_generate_web"),
    path("public/generate/commands/repo/", FormicaView_PublicGenerateViaRepoCommand.as_view(),
         name="public_generate_repo"),
]
