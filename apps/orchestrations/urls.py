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

from apps.orchestrations.views import (OrchestrationView_Create, OrchestrationView_Update, OrchestrationView_QueryList, \
                                       OrchestrationView_List, OrchestrationView_Delete,
                                       OrchestrationView_QueryDelete,
                                       OrchestrationView_QueryDetail, OrchestrationView_QueryRerun)

app_name = "orchestrations"

urlpatterns = [
    path("create/", OrchestrationView_Create.as_view(
        template_name="orchestrations/create_orchestration.html"), name="create"),
    path("list/", OrchestrationView_List.as_view(
        template_name="orchestrations/list_orchestrations.html"), name="list"),
    path("update/<int:pk>/", OrchestrationView_Update.as_view(
        template_name="orchestrations/update_orchestration.html"), name="update"),
    path("delete/<int:pk>/", OrchestrationView_Delete.as_view(
        template_name="orchestrations/delete_orchestration.html"), name="delete"),
    path("query/<int:pk>/list/", OrchestrationView_QueryList.as_view(
        template_name="orchestrations/query_list_orchestration.html"), name="query_list"),
    path("query/<int:pk>/delete/<int:query_id>/", OrchestrationView_QueryDelete.as_view(
        template_name="orchestrations/query_confirm_delete_orchestration.html"), name="query_delete"),
    path("query/<int:pk>/detail/<int:query_id>/", OrchestrationView_QueryDetail.as_view(
        template_name="orchestrations/query_detail_orchestration.html"), name="query_detail"),
    path("query/<int:pk>/rerun/<int:query_id>/", OrchestrationView_QueryRerun.as_view(
        template_name="orchestrations/query_detail_orchestration.html"), name="query_rerun"),
]
