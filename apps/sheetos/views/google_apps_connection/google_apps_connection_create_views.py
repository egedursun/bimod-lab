#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: google_apps_connection_create_views.py
#  Last Modified: 2024-10-31 19:25:44
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 19:25:46
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
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps.assistants.models import Assistant
from apps.sheetos.models import SheetosGoogleAppsConnection
from apps.sheetos.utils import generate_google_apps_connection_api_key


class SheetosView_GoogleAppsConnectionCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        assistant_id = request.POST.get('assistant')
        if not assistant_id:
            messages.error(request, "Assistant field is required.")
            return redirect('sheetos:google_apps_connections_list')

        assistant = get_object_or_404(Assistant, id=assistant_id)

        connection, created = SheetosGoogleAppsConnection.objects.get_or_create(
            owner_user=request.user, sheetos_assistant=assistant,
            defaults={'connection_api_key': generate_google_apps_connection_api_key()}
        )

        if not created:
            messages.warning(request, "A connection for this model already exists. Please renew if necessary.")
        else:
            messages.success(request, "Connection successfully created.")

        return redirect('sheetos:google_apps_connections_list')
