#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: toggle_automated_backups_views.py
#  Last Modified: 2024-10-05 01:39:48
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

import logging

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views import View


logger = logging.getLogger(__name__)


class SettingsView_ToggleAutoBackups(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            user.profile.automated_data_backups = not user.profile.automated_data_backups

            user.profile.save()

        except Exception as e:
            logger.error(f"An error occurred while trying to toggle automated backups: {str(e)}")
            messages.error(request, f"An error occurred while trying to toggle automated backups: {str(e)}")

            return redirect('user_settings:settings')

        logger.info(f"Automated backups have been {'enabled' if user.profile.automated_data_backups else 'disabled'} "
                    f"by User: {user.id}.")

        messages.success(request,
                         f"Automated backups have been {'enabled' if user.profile.automated_data_backups else 'disabled'}.")

        return redirect('user_settings:settings')
