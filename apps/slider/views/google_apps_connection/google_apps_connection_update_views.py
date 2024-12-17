#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: google_apps_connection_update_views.py
#  Last Modified: 2024-11-02 19:40:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 20:10:05
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import (
    get_object_or_404,
    redirect
)

from django.views import View

from apps.assistants.models import Assistant

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.slider.models import (
    SliderGoogleAppsConnection
)

from apps.slider.utils import (
    generate_google_apps_connection_api_key
)

from apps.user_permissions.utils import (
    PermissionNames
)


class SliderView_GoogleAppsConnectionUpdate(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        connection_id = kwargs.get('pk')
        assistant_id = request.POST.get('assistant')

        ##############################
        # PERMISSION CHECK FOR - UPDATE_SLIDER_GOOGLE_APPS_CONNECTIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_SLIDER_GOOGLE_APPS_CONNECTIONS
        ):
            messages.error(self.request, "You do not have permission to update Slider Google Apps Connections.")

            return redirect('slider:google_apps_connections_list')
        ##############################

        try:
            connection = get_object_or_404(
                SliderGoogleAppsConnection,
                id=connection_id,
                owner_user=request.user
            )

            connection.connection_api_key = generate_google_apps_connection_api_key()

            new_assistant = Assistant.objects.get(
                id=assistant_id
            )

            connection.slider_assistant = new_assistant

            connection.save()

        except Exception as e:
            messages.error(request, "An error occurred while updating the API key.")

            return redirect('slider:google_apps_connections_list')

        messages.success(request, "API key successfully updated.")

        return redirect('slider:google_apps_connections_list')
