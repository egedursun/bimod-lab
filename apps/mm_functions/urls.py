#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
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

from apps.mm_functions.views import (CustomFunctionView_Create, CustomFunctionView_List,
                                     CustomFunctionView_Connections, CustomFunctionView_Delete,
                                     CustomFunctionView_Store)

app_name = "mm_functions"

urlpatterns = [
    path(
        "create/",
        CustomFunctionView_Create.as_view(
            template_name="mm_functions/functions/create_custom_function.html"
        ),
        name="create"
    ),

    path(
        "list/",
        CustomFunctionView_List.as_view(
            template_name="mm_functions/functions/list_custom_functions.html"
        ),
        name="list"
    ),

    path(
        "delete/<int:pk>/",
        CustomFunctionView_Delete.as_view(
            template_name="mm_functions/functions/confirm_delete_custom_function.html"
        ),
        name="delete"
    ),

    path(
        "connect/",
        CustomFunctionView_Connections.as_view(
            template_name="mm_functions/connections/manage_assistant_connections.html"
        ),
        name="connect"
    ),

    #####

    path(
        "store/",
        CustomFunctionView_Store.as_view(
            template_name="mm_functions/store/function_store.html"
        ),
        name="store"
    ),
]
