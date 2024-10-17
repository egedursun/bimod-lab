#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_user_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from auth.models import Profile
from auth.utils import is_valid_password, send_verification_email, send_invitation_email
from config import settings
from web_project import TemplateLayout


logger = logging.getLogger(__name__)

class UserManagementView_UserInvite(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_USERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_USERS):
            messages.error(self.request, "You do not have permission to add new users.")
            return redirect('user_management:list')
        ##############################

        username = request.POST.get('username')
        email = request.POST.get('email')
        pw = request.POST.get('password')
        confirm_pw = request.POST.get('confirm_password')
        org = request.POST.get('organization')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_no = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        postal_code = request.POST.get('postal_code')
        is_active = request.POST.get('is_active') == 'on'
        created_by_user = request.user

        try:
            is_valid, message = is_valid_password(pw)
            if not is_valid:
                messages.error(request, message)
                return redirect("user_management:add")
            if pw != confirm_pw:
                messages.error(request, 'Passwords do not match')
                return redirect('user_management:add')

            created_user = User.objects.create_user(username=username, email=email, password=pw)
            created_user.set_password(pw)
            created_user.save()
            user_group, created = Group.objects.get_or_create(name="user")
            created_user.groups.add(user_group)
            token = str(uuid.uuid4())
            user_profile, created = Profile.objects.get_or_create(user=created_user)
            user_profile.email_token = token
            user_profile.email = email
            user_profile.username = username
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.phone_number = phone_no
            user_profile.address = address
            user_profile.city = city
            user_profile.country = country
            user_profile.postal_code = postal_code
            user_profile.is_active = is_active
            user_profile.organization = Organization.objects.get(id=org)
            user_profile.created_by_user = created_by_user
            user_profile.save()

            org = Organization.objects.get(id=org)
            org.users.add(created_user)
            org.save()
            created_by_user.profile.sub_users.add(created_user)
            created_by_user.profile.save()
            send_verification_email(email, token)
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                logger.info(f"Verification email sent to {email}")
                messages.success(request, "Verification email sent successfully.")
            else:
                logger.error("Email settings are not configured. Unable to send verification email.")
                messages.error(request, "Email settings are not configured. Unable to send verification email.")
            messages.success(request, 'User created successfully!')
            logger.info(f"User: {created_user.id} was created by User: {created_by_user.id}.")

            try:
                email = created_user.email
                send_invitation_email(email, token)
                if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                    logger.info(f"Invitation email sent to {email}")
                    messages.success(request, 'Invitation email sent successfully!')
                else:
                    logger.error('Email settings are not configured. Unable to send invitation email.')
                    messages.error(request, 'Email settings are not configured. Unable to send invitation email.')
                messages.success(request, 'Invitation email sent successfully!')
                logger.info(f"User: {created_user.id} was created by User: {created_by_user.id}.")
            except Exception as e:
                logger.error(f'Error sending invitation email: {str(e)}')
                messages.error(request, f'Error sending invitation email: {str(e)}')
        except Exception as e:
            logger.error(f'Error creating user: {str(e)}')
            messages.error(request, f'Error creating user: {str(e)}')
        return redirect('user_management:list')
