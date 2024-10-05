#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: rerun_orchestration_query_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:39
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
#  File: rerun_orchestration_query_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:07:12
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps._services.orchestration.orchestration_executor import OrchestrationExecutor
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.orchestrations.models import OrchestrationQueryLog
from apps.orchestrations.models.query import OrchestrationQuery
from apps.orchestrations.utils import OrchestrationQueryLogTypesNames
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class OrchestrationQueryRerunView(LoginRequiredMixin, TemplateView):
    template_name = "orchestrations/query_detail_orchestration.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        #############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_ORCHESTRATION_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_AND_USE_ORCHESTRATION_CHATS):
            messages.error(self.request, "You do not have permission to create and use orchestration queries.")
            return redirect('orchestrations:list')
        ##############################

        query_id = self.kwargs.get('query_id')
        query = get_object_or_404(OrchestrationQuery, id=query_id)

        query_text = query.query_text

        # delete all previous logs
        query.logs.all().delete()

        # add a new log for the user query
        query_log = OrchestrationQueryLog.objects.create(
            orchestration_query=query,
            log_type=OrchestrationQueryLogTypesNames.USER,
            log_text_content=query_text,
            log_file_contents=None,
            log_image_contents=None,
        )
        query.logs.add(query_log)
        query.save()

        # re-run the query
        orchestration_executor = OrchestrationExecutor(
            maestro=query.maestro,
            query_chat=query
        )
        final_response = orchestration_executor.execute_for_query()
        print("[OrchestrationQueryRerunView.get_context_data] Final response retrieved: ", final_response)

        return redirect('orchestrations:query_detail', pk=query.maestro.id, query_id=query.id)
