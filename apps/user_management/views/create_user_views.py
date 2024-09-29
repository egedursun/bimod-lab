#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: create_user_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:10:04
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

import uuid

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from auth.helpers import send_verification_email, send_invitation_email
from auth.models import Profile
from config import settings
from web_project import TemplateLayout


class AddNewUserView(LoginRequiredMixin, TemplateView):
    """
    View to add an existing user to an organization.

    This view allows administrators to add existing users (sub-users) to an organization that the administrator belongs to.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the list of sub-users and organizations the user can manage.
        post(self, request, *args, **kwargs): Handles the logic to add a user to the selected organization.
    """

    template_name = "user_management/users/add_new_user.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_USERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_USERS):
            messages.error(self.request, "You do not have permission to add new users.")
            return redirect('user_management:list')
        ##############################

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        organization = request.POST.get('organization')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        postal_code = request.POST.get('postal_code')
        is_active = request.POST.get('is_active') == 'on'
        created_by_user = request.user

        try:
            # validate the password
            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return redirect('user_management:add')

            created_user = User.objects.create_user(username=username, email=email, password=password)
            created_user.set_password(password)
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
            user_profile.phone_number = phone_number
            user_profile.address = address
            user_profile.city = city
            user_profile.country = country
            user_profile.postal_code = postal_code
            user_profile.is_active = is_active
            user_profile.organization = Organization.objects.get(id=organization)
            user_profile.created_by_user = created_by_user
            user_profile.save()

            # add user to the organization
            organization = Organization.objects.get(id=organization)
            organization.users.add(created_user)
            organization.save()
            # add user as a subuser to the user
            created_by_user.profile.sub_users.add(created_user)
            created_by_user.profile.save()
            send_verification_email(email, token)
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                messages.success(request, "Verification email sent successfully.")
            else:
                messages.error(request, "Email settings are not configured. Unable to send verification email.")
            messages.success(request, 'User created successfully!')

            try:
                email = created_user.email
                send_invitation_email(email, token)
                if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                    messages.success(request, 'Invitation email sent successfully!')
                else:
                    messages.error(request, 'Email settings are not configured. Unable to send invitation email.')
                messages.success(request, 'Invitation email sent successfully!')
            except Exception as e:
                messages.error(request, f'Error sending invitation email: {str(e)}')

            print('[AddNewUserView.post] User created successfully.')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
        return redirect('user_management:list')
