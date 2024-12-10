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

from apps.slider.views.google_apps_connection import (
    SliderView_GoogleAppsConnectionList,
    SliderView_GoogleAppsConnectionCreate,
    SliderView_GoogleAppsConnectionDelete,
    SliderView_GoogleAppsConnectionUpdate
)

from apps.slider.views.public import (
    SliderView_PublicGenerateViaAICommand,
    SliderView_PublicGenerateViaNoSQLCommand,
    SliderView_PublicGenerateViaSQLCommand,
    SliderView_PublicGenerateViaSSHCommand,
    SliderView_PublicGenerateViaSelectCommand,
    SliderView_PublicGenerateViaVectCommand,
    SliderView_PublicGenerateViaAutoCommand,
    SliderView_PublicGenerateViaImgCommand,
    SliderView_PublicGenerateViaWebCommand,
    SliderView_PublicGenerateViaRepoCommand,
    SliderView_PublicGenerateViaSiteCommand,
)

app_name = 'slider'

urlpatterns = [
    # Google Apps Connections
    path(
        "google_apps/connections/list/",
        SliderView_GoogleAppsConnectionList.as_view(
            template_name="slider/google_apps_connection/manage_google_apps_connections.html"
        ),
        name="google_apps_connections_list"
    ),

    path(
        "google_apps/connections/create/",
        SliderView_GoogleAppsConnectionCreate.as_view(

        ),
        name="google_apps_connections_create"
    ),

    path(
        "google_apps/connections/update/<int:pk>/",
        SliderView_GoogleAppsConnectionUpdate.as_view(

        ),
        name="google_apps_connections_update"
    ),

    path(
        "google_apps/connections/delete/<int:pk>/",
        SliderView_GoogleAppsConnectionDelete.as_view(

        ),
        name="google_apps_connections_delete"
    ),

    #####

    # Public endpoints

    path(
        "public/generate/commands/ai/",
        SliderView_PublicGenerateViaAICommand.as_view(

        ),
        name="public_generate_ai"
    ),

    path(
        "public/generate/commands/nosql/",
        SliderView_PublicGenerateViaNoSQLCommand.as_view(

        ),
        name="public_generate_nosql"
    ),

    path(
        "public/generate/commands/sql/",
        SliderView_PublicGenerateViaSQLCommand.as_view(

        ),
        name="public_generate_sql"
    ),

    path(
        "public/generate/commands/ssh/",
        SliderView_PublicGenerateViaSSHCommand.as_view(

        ),
        name="public_generate_ssh"
    ),

    path(
        "public/generate/commands/select/",
        SliderView_PublicGenerateViaSelectCommand.as_view(

        ),
        name="public_generate_select"
    ),

    path(
        "public/generate/commands/vect/",
        SliderView_PublicGenerateViaVectCommand.as_view(

        ),
        name="public_generate_vect"
    ),

    path(
        "public/generate/commands/auto/",
        SliderView_PublicGenerateViaAutoCommand.as_view(

        ),
        name="public_generate_auto"
    ),

    path(
        "public/generate/commands/img/",
        SliderView_PublicGenerateViaImgCommand.as_view(

        ),
        name="public_generate_img"
    ),

    path(
        "public/generate/commands/web/",
        SliderView_PublicGenerateViaWebCommand.as_view(

        ),
        name="public_generate_web"
    ),

    path(
        "public/generate/commands/repo/",
        SliderView_PublicGenerateViaRepoCommand.as_view(

        ),
        name="public_generate_repo"
    ),

    path(
        "public/generate/commands/site/",
        SliderView_PublicGenerateViaSiteCommand.as_view(

        ),
        name="public_generate_site"
    ),
]
