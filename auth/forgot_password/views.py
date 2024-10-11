#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: views.py
#  Last Modified: 2024-10-05 15:31:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 15:45:58
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

from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from auth.utils import send_password_reset_email
from auth.models import Profile
from auth.views import AuthView
from datetime import timedelta, datetime
import uuid


class ForgetPasswordView(AuthView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard:main-dashboard")
        return super().get(request)

    def post(self, request):
        if request.method == "POST":
            email = request.POST.get("email")
            user = User.objects.filter(email=email).first()
            if not user:
                messages.error(request, "No user with this email exists.")
                return redirect("forgot-password")
            token = str(uuid.uuid4())
            expiration_time = datetime.now() + timedelta(hours=24)
            user_profile, created = Profile.objects.get_or_create(user=user)
            user_profile.forget_password_token = token
            user_profile.forget_password_token_expiration = expiration_time
            user_profile.save()
            send_password_reset_email(email, token)
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                messages.success(request, "A password reset email has been sent. Please check your inbox")
            else:
                messages.error(request, "Email settings are not configured. Unable to send verification email.")
            return redirect("forgot-password")
