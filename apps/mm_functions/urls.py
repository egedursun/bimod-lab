#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:37
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
#  Last Modified: 2024-08-02 11:55:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:01:50
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.mm_functions.views import (CreateCustomFunctionView, ListCustomFunctionsView,
                                     ManageCustomFunctionAssistantConnectionsView, DeleteCustomFunctionView,
                                     FunctionStoreView)

app_name = "mm_functions"

urlpatterns = [
    path("create/", CreateCustomFunctionView.as_view(
        template_name="mm_functions/functions/create_custom_function.html"
    ), name="create"),
    path("list/", ListCustomFunctionsView.as_view(
        template_name="mm_functions/functions/list_custom_functions.html"
    ), name="list"),
    path("delete/<int:pk>/", DeleteCustomFunctionView.as_view(
        template_name="mm_functions/functions/confirm_delete_custom_function.html"
    ), name="delete"),

    path("connect/", ManageCustomFunctionAssistantConnectionsView.as_view(
        template_name="mm_functions/connections/manage_assistant_connections.html"
    ), name="connect"),

    path("store/", FunctionStoreView.as_view(
        template_name="mm_functions/store/function_store.html"
    ), name="store"),
]
