#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: urls.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.urls import path

from apps.orchestrations.views import (CreateOrchestrationView, OrchestrationUpdateView, OrchestrationQueryListView, \
                                       OrchestrationListView, OrchestrationDeleteView,
                                       OrchestrationQueryDeleteView,
                                       OrchestrationQueryDetailView, OrchestrationQueryRerunView)

app_name = "orchestrations"

urlpatterns = [
    path("create/", CreateOrchestrationView.as_view(
        template_name="orchestrations/create_orchestration.html"), name="create"),
    path("list/", OrchestrationListView.as_view(
        template_name="orchestrations/list_orchestrations.html"), name="list"),
    path("update/<int:pk>/", OrchestrationUpdateView.as_view(
        template_name="orchestrations/update_orchestration.html"), name="update"),
    path("delete/<int:pk>/", OrchestrationDeleteView.as_view(
        template_name="orchestrations/delete_orchestration.html"), name="delete"),
    ##############################
    path("query/<int:pk>/list/", OrchestrationQueryListView.as_view(
        template_name="orchestrations/query_list_orchestration.html"), name="query_list"),
    path("query/<int:pk>/delete/<int:query_id>/", OrchestrationQueryDeleteView.as_view(
        template_name="orchestrations/query_confirm_delete_orchestration.html"), name="query_delete"),
    path("query/<int:pk>/detail/<int:query_id>/", OrchestrationQueryDetailView.as_view(
        template_name="orchestrations/query_detail_orchestration.html"), name="query_detail"),
    path("query/<int:pk>/rerun/<int:query_id>/", OrchestrationQueryRerunView.as_view(
        template_name="orchestrations/query_detail_orchestration.html"), name="query_rerun"),
]
