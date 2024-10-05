#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

import uuid

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from auth.helpers import send_password_reset_email
from config import settings
from web_project import TemplateLayout


class UserProfileResetPasswordView(LoginRequiredMixin, TemplateView):
    """
    Sends a password reset email to the user.

    GET:
    - Fetches the user based on the provided primary key (pk).
    - Generates a password reset token and sends a reset email to the user's email address.
    - Displays success or error messages depending on the email sending status.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['pk'] = self.kwargs.get('pk')
        print('[UserProfileResetPasswordView.get_context_data] PK:', context['pk'])
        return context

    def get(self, request, *args, **kwargs):
        pk = self.get_context_data()['pk']
        try:
            user = User.objects.get(pk=pk)
            email = user.email
            token = str(uuid.uuid4())
            send_password_reset_email(email, token)
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                print('[UserProfileResetPasswordView.get] Password reset email sent successfully!')
                messages.success(request, 'Password reset email sent successfully!')
            else:
                print(
                    '[UserProfileResetPasswordView.get] Email settings are not configured. Unable to send verification email.')
                messages.error(request, 'Email settings are not configured. Unable to send verification email.')
            print('[UserProfileResetPasswordView.get] Password reset email sent successfully.')
            messages.success(request, 'Password reset email sent successfully!')
        except Exception as e:
            messages.error(request, f'Failed to send password reset email: {e}')
        print('[UserProfileResetPasswordView.get] Password reset email sent successfully.')
        return self.render_to_response(self.get_context_data())
