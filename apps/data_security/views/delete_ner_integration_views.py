#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_ner_integration_views.py
#  Last Modified: 2024-10-05 01:39:47
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
#
#
#
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.data_security.models import NERIntegration
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class NERView_IntegrationDelete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        ner_integration = get_object_or_404(NERIntegration, id=self.kwargs['pk'])
        context['ner_integration'] = ner_integration
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_DATA_SECURITY
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_DATA_SECURITY):
            messages.error(self.request, "You do not have permission to delete data security layers.")
            return redirect('data_security:list_ner_integrations')
        ##############################

        ner_integration = get_object_or_404(NERIntegration, id=self.kwargs['pk'])
        ner_integration.delete()
        logger.info(f"User: {request.user} - NER Integration: {ner_integration.name} - Deleted.")
        messages.success(request, 'NER Policy has been deleted successfully.')
        return redirect('data_security:list_ner_integrations')
