#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: google_apps_connection_delete_views.py
#  Last Modified: 2024-10-31 03:23:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 03:23:41
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
from django.views import View

from apps.drafting.models import DraftingGoogleAppsConnection


class DraftingView_GoogleAppsConnectionDelete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        connection_id = kwargs.get('pk')
        connection = get_object_or_404(DraftingGoogleAppsConnection, id=connection_id, owner_user=request.user)

        try:
            connection.delete()
        except Exception as e:
            messages.error(request, "An error occurred while deleting the connection.")
            return redirect('drafting:google_apps_connections_list')

        messages.success(request, "Connection successfully deleted.")
        return redirect('drafting:google_apps_connections_list')
