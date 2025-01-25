#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-12-23 09:35:11
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-23 09:35:11
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.urls import (
    path
)

from apps.browser_extensions.views import (
    BrowserExtensionsView_ChromeExtensionConnectionPage,
    BrowserExtensionsView_ChromeExtensionConnectionCreate,
    BrowserExtensionsView_ChromeExtensionConnectionUpdate,
    BrowserExtensionsView_ChromeExtensionConnectionDelete,
    BrowserExtensionView_PublicGenerateViaSiteCommand,
    BrowserExtensionView_PublicGenerateViaRepoCommand,
    BrowserExtensionView_PublicGenerateViaWebCommand,
    BrowserExtensionView_PublicGenerateViaVectCommand,
    BrowserExtensionView_PublicGenerateViaSSHCommand,
    BrowserExtensionView_PublicGenerateViaSQLCommand,
    BrowserExtensionView_PublicGenerateViaNoSQLCommand,
    BrowserExtensionView_PublicGenerateViaAICommand,
)

app_name = 'browser_extensions'

urlpatterns = [
    path(
        'google_apps/connections/list/',
        BrowserExtensionsView_ChromeExtensionConnectionPage.as_view(
            template_name='browser_extensions/chrome/chrome_extension_connection_page.html'
        ),
        name='google_apps_connections_list'
    ),

    path(
        "google_apps/connections/create/",
        BrowserExtensionsView_ChromeExtensionConnectionCreate.as_view(

        ),
        name="google_apps_connections_create"
    ),

    path(
        "google_apps/connections/update/<int:pk>/",
        BrowserExtensionsView_ChromeExtensionConnectionUpdate.as_view(

        ),
        name="google_apps_connections_update"
    ),

    path(
        "google_apps/connections/delete/<int:pk>/",
        BrowserExtensionsView_ChromeExtensionConnectionDelete.as_view(

        ),
        name="google_apps_connections_delete"
    ),

    #####

    # Public endpoints

    path(
        "public/generate/commands/ai/",
        BrowserExtensionView_PublicGenerateViaAICommand.as_view(

        ),
        name="public_generate_ai"
    ),

    path(
        "public/generate/commands/nosql/",
        BrowserExtensionView_PublicGenerateViaNoSQLCommand.as_view(

        ),
        name="public_generate_nosql"
    ),

    path(
        "public/generate/commands/sql/",
        BrowserExtensionView_PublicGenerateViaSQLCommand.as_view(

        ),
        name="public_generate_sql"
    ),

    path(
        "public/generate/commands/ssh/",
        BrowserExtensionView_PublicGenerateViaSSHCommand.as_view(

        ),
        name="public_generate_ssh"
    ),

    path(
        "public/generate/commands/vect/",
        BrowserExtensionView_PublicGenerateViaVectCommand.as_view(

        ),
        name="public_generate_vect"
    ),

    path(
        "public/generate/commands/web/",
        BrowserExtensionView_PublicGenerateViaWebCommand.as_view(

        ),
        name="public_generate_web"
    ),

    path(
        "public/generate/commands/repo/",
        BrowserExtensionView_PublicGenerateViaRepoCommand.as_view(

        ),
        name="public_generate_repo"
    ),

    path(
        "public/generate/commands/site/",
        BrowserExtensionView_PublicGenerateViaSiteCommand.as_view(

        ),
        name="public_generate_site"
    ),
]
