#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: confirm_delete_metatempo_connection_views.py
#  Last Modified: 2024-10-28 20:29:36
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:29:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.metatempo.models import MetaTempoConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class MetaTempoView_ConnectionConfirmDelete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        connection_id = kwargs['connection_id']
        connection = get_object_or_404(MetaTempoConnection, id=connection_id)
        context['connection'] = connection
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_METATEMPO_CONNECTION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_METATEMPO_CONNECTION):
            messages.error(self.request, "You do not have permission to delete a MetaTempo Connection.")
            return redirect('metatempo:connection_list')
        ##############################

        connection_id = kwargs['connection_id']
        connection = get_object_or_404(MetaTempoConnection, id=connection_id)
        connection.delete()
        messages.success(request, "MetaTempo Connection deleted successfully.")
        return redirect("metatempo:connection_list")
