#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: views.py
#  Last Modified: 2024-10-05 15:31:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 15:45:58
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from django.shortcuts import redirect

from django.contrib.auth import (
    authenticate,
    login
)

from django.contrib.auth.models import (
    User
)

from django.contrib import messages
from auth.views import AuthView


class LoginView(AuthView):
    def get(self, request):

        if request.user.is_authenticated:
            return redirect("dashboard:lab-landing")

        return super().get(request)

    def post(self, request):
        if request.method == "POST":
            username = request.POST.get("email-username")
            password = request.POST.get("password")

            if not (username and password):
                messages.error(request, "Please enter your username and password.")
                return redirect("login")

            if "@" in username:
                user_email = User.objects.filter(
                    email=username
                ).first()

                if user_email is None:
                    messages.error(request, "Please enter a valid email.")

                    return redirect("login")

                username = user_email.username

            user_email = User.objects.filter(
                username=username
            ).first()

            if user_email is None:
                messages.error(request, "No user with this username exists in the system.")

                return redirect("login")

            authenticated_user = authenticate(
                request,
                username=username,
                password=password
            )

            if authenticated_user is not None:

                try:
                    login(
                        request,
                        authenticated_user
                    )

                except Exception as e:
                    messages.error(request, "An error occurred while trying to log in. Please try again.")

                    return redirect("login")

                if "next" in request.POST:

                    return redirect(request.POST["next"])

                else:

                    return redirect("dashboard:lab-landing")

            else:
                messages.error(request, "Either the username or password is incorrect. Please try again.")

                return redirect("login")
