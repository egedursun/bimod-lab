#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: rerun_orchestration_query_views.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import (
    redirect,
    get_object_or_404
)

from django.views.generic import TemplateView

from apps.core.orchestration.orchestration_executor import (
    OrchestrationExecutor
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.orchestrations.models import (
    OrchestrationQueryLog
)

from apps.orchestrations.models.query import (
    OrchestrationQuery
)

from apps.orchestrations.utils import (
    OrchestrationQueryLogTypesNames
)

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class OrchestrationView_QueryRerun(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        #############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_ORCHESTRATION_CHATS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.CREATE_AND_USE_ORCHESTRATION_CHATS
        ):
            messages.error(self.request, "You do not have permission to create and use orchestration queries.")

            return redirect('orchestrations:list')
        ##############################

        query_id = self.kwargs.get('query_id')

        query = get_object_or_404(
            OrchestrationQuery,
            id=query_id
        )

        query_text = query.query_text

        attached_images = request.FILES.getlist(
            'attached_images[]',
            []
        )

        attached_files = request.FILES.getlist(
            'attached_files[]',
            []
        )

        try:
            query.logs.all().delete()

            query_log = OrchestrationQueryLog.objects.create(
                orchestration_query=query,
                log_type=OrchestrationQueryLogTypesNames.USER,
                log_text_content=query_text + f"""
                            -----

                            **IMAGE URLS:**
                            '''
                            {attached_images}
                            '''

                            -----

                            **FILE URLS:**
                            '''
                            {attached_files}
                            '''

                            -----
                        """,
                log_file_contents=attached_files,
                log_image_contents=attached_images
            )

            query.logs.add(query_log)

            query.save()

            orch_xc = OrchestrationExecutor(
                maestro=query.maestro,
                query_chat=query
            )

            final_response = orch_xc.execute_for_query()

        except Exception as e:
            messages.error(request, f"An error occurred while rerunning the Orchestration Query: {str(e)}")

            return redirect(
                "orchestrations:query_detail",
                pk=query.maestro.id,
                query_id=query.id
            )

        logger.info(f"Orchestration query was rerun by User: {self.request.user.id}.")

        return redirect(
            'orchestrations:query_detail',
            pk=query.maestro.id,
            query_id=query.id
        )
