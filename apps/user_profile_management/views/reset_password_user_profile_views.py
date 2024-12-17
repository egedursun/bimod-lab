#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: reset_password_user_profile_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:47
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
import uuid

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.contrib.auth.models import User

from django.views.generic import TemplateView

from auth.utils import (
    send_password_reset_email
)

from config import settings
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class UserProfileView_ResetPassword(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['pk'] = self.kwargs.get('pk')

        return context

    def get(self, request, *args, **kwargs):
        pk = self.get_context_data()['pk']

        try:
            user = User.objects.get(
                pk=pk
            )

            email = user.email
            token = str(uuid.uuid4())

            send_password_reset_email(
                email,
                token
            )

            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                logger.info(f"Password reset email sent to {email}")
                messages.success(request, 'Password reset email sent successfully!')

            else:
                logger.error("Email settings are not configured. Unable to send verification email.")
                messages.error(request, 'Email settings are not configured. Unable to send verification email.')

            logger.info(f"Password reset email sent to {email}")
            messages.success(request, 'Password reset email sent successfully!')

        except Exception as e:
            logger.error(f'Failed to send password reset email: {e}')
            messages.error(request, f'Failed to send password reset email: {e}')

        return self.render_to_response(
            self.get_context_data()
        )
