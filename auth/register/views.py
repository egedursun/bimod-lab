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
#

from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.conf import settings

from apps.notifications.models import NotificationItem
from apps.notifications.utils import NotificationTitleCategoryChoicesNames, NotificationFAIconChoicesNames
from auth.utils import is_valid_password, send_verification_email
from auth.views import AuthView
from auth.models import Profile
import uuid


class RegisterView(AuthView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard:main-dashboard")
        context = self.get_context_data()
        return super().get(request, context)

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # check if the username and email are unique
        if User.objects.filter(username=username).exists():
            messages.error(request, "User with this username already exists.")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists.")
            return redirect("register")

        is_valid, message = is_valid_password(password)
        if not is_valid:
            messages.error(request, message)
            return redirect("register")
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_number = request.POST.get("phone_number")
        birthdate = request.POST.get("birthdate")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        postal_code = request.POST.get("postal_code")
        profile_picture = request.FILES.get("profile_picture")
        if User.objects.filter(username=username, email=email).exists():
            messages.error(request, "User already exists, Try logging in.")
            return redirect("register")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        created_user = User.objects.create_user(username=username, email=email, password=password)
        created_user.set_password(password)
        created_user.is_staff = False
        created_user.is_superuser = True
        created_user.save()
        user_group, created = Group.objects.get_or_create(name="tenant")
        created_user.groups.add(user_group)
        token = str(uuid.uuid4())
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
        user_profile.free_credits = settings.NEW_USER_FREE_CREDITS if hasattr(settings, 'NEW_USER_FREE_CREDITS') else 0
        primary_admin = User.objects.filter(username="admin").first()
        user_profile.created_by_user = primary_admin
        user_profile.save()
        send_verification_email(email, token)
        if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            messages.success(request, "Verification email sent successfully")
        else:
            messages.error(request, "Email settings are not configured. Unable to send verification email.")
        request.session['email'] = email

        welcome_notification = NotificationItem.objects.create(
            user=created_user,
            notification_title_category=NotificationTitleCategoryChoicesNames.HumanReadable.BIMOD_TEAM,
            notification_fa_icon=NotificationFAIconChoicesNames.BUILDING,
            notification_message="Welcome to the platform! We have sent you a verification email, and we recommend you"
                                 " to verify your email address for your own security and privacy. If you need help,"
                                 " please contact us via the support page.")
        user_profile.user.notifications.set([welcome_notification])

        return redirect("verify-email-page")
