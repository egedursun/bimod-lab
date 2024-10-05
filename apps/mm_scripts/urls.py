#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: urls.py
#  Last Modified: 2024-08-02 12:17:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:03:49
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.mm_scripts.views import CreateCustomScriptView, ListCustomScriptsView, \
    ManageCustomScriptAssistantConnectionsView, DeleteCustomScriptView, ScriptStoreView

app_name = "mm_scripts"

urlpatterns = [
    path("create/", CreateCustomScriptView.as_view(
        template_name="mm_scripts/scripts/create_custom_script.html"
    ), name="create"),
    path("list/", ListCustomScriptsView.as_view(
        template_name="mm_scripts/scripts/list_custom_scripts.html"
    ), name="list"),
    path("delete/<int:pk>/", DeleteCustomScriptView.as_view(
        template_name="mm_scripts/scripts/confirm_delete_custom_script.html"
    ), name="delete"),

    path("connect/", ManageCustomScriptAssistantConnectionsView.as_view(
        template_name="mm_scripts/connections/manage_script_connections.html"
    ), name="connect"),

    path("store/", ScriptStoreView.as_view(
        template_name="mm_scripts/store/script_store.html"
    ), name="store"),
]
