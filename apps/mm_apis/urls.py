#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: urls.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:32
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
#  Created: 2024-09-28 23:00:51
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.urls import path

from apps.mm_apis.views import CreateCustomAPIView, ListCustomAPIsView, DeleteCustomAPIView, APIStoreView, \
    ManageCustomAPIAssistantConnectionsView

app_name = "mm_apis"

urlpatterns = [
    path("create/", CreateCustomAPIView.as_view(
        template_name="mm_apis/apis/create_custom_api.html"
    ), name="create"),
    path("list/", ListCustomAPIsView.as_view(
        template_name="mm_apis/apis/list_custom_apis.html"
    ), name="list"),
    path("delete/<int:pk>/", DeleteCustomAPIView.as_view(
        template_name="mm_apis/apis/confirm_delete_custom_api.html"
    ), name="delete"),

    path("connect/", ManageCustomAPIAssistantConnectionsView.as_view(
        template_name="mm_apis/connections/manage_api_connections.html"
    ), name="connect"),

    path("store/", APIStoreView.as_view(
        template_name="mm_apis/store/api_store.html"
    ), name="store"),
]
