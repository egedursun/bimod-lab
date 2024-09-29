#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: views.py
#  Last Modified: 2024-08-03 12:38:40
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:13:32
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from auth.views import AuthView


class LoginView(AuthView):
    def get(self, request):
        if request.user.is_authenticated:
            # If the user is already logged in, redirect them to the home page or another appropriate page.
            return redirect("dashboard:main-dashboard")
        # Render the login page for users who are not logged in.
        return super().get(request)

    def post(self, request):
        if request.method == "POST":
            username = request.POST.get("email-username")
            password = request.POST.get("password")
            if not (username and password):
                messages.error(request, "Please enter your username and password.")
                return redirect("login")
            if "@" in username:
                user_email = User.objects.filter(email=username).first()
                if user_email is None:
                    messages.error(request, "Please enter a valid email.")
                    return redirect("login")
                username = user_email.username
            user_email = User.objects.filter(username=username).first()
            if user_email is None:
                messages.error(request, "No user with this username exists in the system.")
                return redirect("login")
            authenticated_user = authenticate(request, username=username, password=password)
            if authenticated_user is not None:
                # Login the user if authentication is successful
                login(request, authenticated_user)
                # Redirect to the page the user was trying to access before logging in
                if "next" in request.POST:
                    return redirect(request.POST["next"])
                else:  # Redirect to the home page or another appropriate page
                    return redirect("dashboard:main-dashboard")
            else:
                messages.error(request, "Either the username or password is incorrect. Please try again.")
                return redirect("login")
