#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: delete_orchestration_query_views.py
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

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.orchestrations.models.query import OrchestrationQuery
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class OrchestrationQueryDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'orchestrations/query_confirm_delete_orchestration.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        query_id = self.kwargs['query_id']
        context['query'] = get_object_or_404(OrchestrationQuery, pk=query_id)
        context['orchestration'] = context['query'].maestro
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - REMOVE_ORCHESTRATION_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_ORCHESTRATION_CHATS):
            messages.error(self.request, "You do not have permission to remove orchestration queries.")
            return redirect('orchestrations:list')
        ##############################

        query_id = self.kwargs['query_id']
        query = get_object_or_404(OrchestrationQuery, pk=query_id)
        maestro_id = query.maestro.id
        query.delete()
        return redirect('orchestrations:query_list', pk=maestro_id)
