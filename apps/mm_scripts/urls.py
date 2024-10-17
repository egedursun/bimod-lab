#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

#

from django.urls import path

from apps.mm_scripts.views import CustomScriptView_Create, CustomScriptView_List, \
    CustomScriptView_Connections, CustomScriptView_Delete, CustomScriptView_Store

app_name = "mm_scripts"

urlpatterns = [
    path("create/", CustomScriptView_Create.as_view(
        template_name="mm_scripts/scripts/create_custom_script.html"), name="create"),
    path("list/", CustomScriptView_List.as_view(
        template_name="mm_scripts/scripts/list_custom_scripts.html"), name="list"),
    path("delete/<int:pk>/", CustomScriptView_Delete.as_view(
        template_name="mm_scripts/scripts/confirm_delete_custom_script.html"), name="delete"),
    path("connect/", CustomScriptView_Connections.as_view(
        template_name="mm_scripts/connections/manage_script_connections.html"), name="connect"),
    path("store/", CustomScriptView_Store.as_view(
        template_name="mm_scripts/store/script_store.html"), name="store"),
]
