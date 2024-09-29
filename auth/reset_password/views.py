#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: views.py
#  Last Modified: 2024-08-03 12:38:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:13:42
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.shortcuts import render, redirect
from django.contrib import messages
from auth.models import Profile
from auth.views import AuthView
from django.contrib.auth import authenticate, login


class ResetPasswordView(AuthView):
    def get(self, request, token):
        if request.user.is_authenticated:
            # If the user is already logged in, redirect them to the home page or another appropriate page.
            return redirect("dashboard:main-dashboard")
        # Render the login page for users who are not logged in.
        return super().get(request)

    def post(self, request, token):
        try:
            profile = Profile.objects.get(forget_password_token=token)
        except Profile.DoesNotExist:
            messages.error(request, "Invalid or expired token.")
            return redirect("forgot-password")

        if request.method == "POST":
            new_password = request.POST.get("password")
            confirm_password = request.POST.get("confirm-password")
            if not (new_password and confirm_password):
                messages.error(request, "Please fill all fields.")
                return render(request, "reset-password")
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, "reset-password")
            user = profile.user
            user.set_password(new_password)
            user.save()
            # Clear the forget_password_token
            profile.forget_password_token = ""
            profile.save()
            # Log the user in after a successful password reset
            authenticated_user = authenticate(request, username=user.username, password=new_password)
            if authenticated_user:
                login(request, authenticated_user)
                return redirect("dashboard:main-dashboard")
            else:
                messages.success(request, "Password reset successful. Please log in.")
                return redirect("login")
