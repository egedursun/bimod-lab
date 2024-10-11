#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.urls import path

from apps.mm_apis.views import CustomAPIView_Create, CustomAPIView_List, CustomAPIView_Delete, CustomAPIView_Store, \
    CustomAPIView_Connections

app_name = "mm_apis"

urlpatterns = [
    path("create/", CustomAPIView_Create.as_view(template_name="mm_apis/apis/create_custom_api.html"), name="create"),
    path("list/", CustomAPIView_List.as_view(template_name="mm_apis/apis/list_custom_apis.html"), name="list"),
    path("delete/<int:pk>/", CustomAPIView_Delete.as_view(template_name="mm_apis/apis/confirm_delete_custom_api.html"),
         name="delete"),
    path("connect/", CustomAPIView_Connections.as_view(
        template_name="mm_apis/connections/manage_api_connections.html"), name="connect"),
    path("store/", CustomAPIView_Store.as_view(template_name="mm_apis/store/api_store.html"), name="store"),
]
