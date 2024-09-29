#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: views.py
#  Last Modified: 2024-09-05 11:16:22
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:13:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.conf import settings
from auth.views import AuthView
from auth.helpers import send_verification_email
from auth.models import Profile
import uuid


class RegisterView(AuthView):
    def get(self, request):
        if request.user.is_authenticated:
            # If the user is already logged in, redirect them to the home page or another appropriate page.
            return redirect("dashboard:main-dashboard")
        # Render the login page for users who are not logged in.
        # get the context
        context = self.get_context_data()
        return super().get(request, context)

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        # Check if the passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")
        ########################################
        # ADDITIONAL INFORMATION
        ########################################
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        birthdate = request.POST.get("birthdate")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        postal_code = request.POST.get("postal_code")
        profile_picture = request.FILES.get("profile_picture")
        ########################################
        # Check if a user with the same username or email already exists
        if User.objects.filter(username=username, email=email).exists():
            messages.error(request, "User already exists, Try logging in.")
            return redirect("register")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")
        # Create the user and set their password
        created_user = User.objects.create_user(username=username, email=email, password=password)
        created_user.set_password(password)
        # grant admin privileges
        created_user.is_staff = False
        created_user.is_superuser = True
        created_user.save()
        # Add the user to the 'client' group (or any other group you want to use as default for new users)
        user_group, created = Group.objects.get_or_create(name="tenant")
        created_user.groups.add(user_group)
        # Generate a token and send a verification email here
        token = str(uuid.uuid4())
        # Set the token in the user's profile
        user_profile, created = Profile.objects.get_or_create(user=created_user)
        user_profile.email_token = token
        user_profile.email = email
        user_profile.username = username
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.phone_number = phone_number
        user_profile.birthdate = birthdate
        user_profile.address = address
        user_profile.city = city
        user_profile.country = country
        user_profile.postal_code = postal_code
        user_profile.profile_picture = profile_picture

        # check the free credits status from the settings
        user_profile.free_credits = settings.NEW_USER_FREE_CREDITS if hasattr(settings, 'NEW_USER_FREE_CREDITS') else 0

        # Get the primary admin (1)
        primary_admin = User.objects.filter(username="admin").first()
        user_profile.created_by_user = primary_admin
        user_profile.save()
        send_verification_email(email, token)
        if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            messages.success(request, "Verification email sent successfully")
        else:
            messages.error(request, "Email settings are not configured. Unable to send verification email.")
        request.session['email'] = email  ## Save email in session
        # Redirect to the verification page after successful registration
        return redirect("verify-email-page")
