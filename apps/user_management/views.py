import uuid
from pprint import pprint

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from apps.organization.models import Organization
from apps.user_management.forms import UserStatusForm
from auth.helpers import send_verification_email
from auth.models import Profile
from config import settings
from web_project import TemplateLayout


# Create your views here.


class AddNewUserView(LoginRequiredMixin, TemplateView):
    template_name = "user_management/add_new_user.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        return context

    def post(self, request, *args, **kwargs):
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
            user_group, created = Group.objects.get_or_create(name="client")
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

            send_verification_email(email, token)
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                messages.success(request, "Verification email sent successfully.")
            else:
                messages.error(request, "Email settings are not configured. Unable to send verification email.")
            messages.success(request, 'User created successfully!')
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')

        return redirect('user_management:add')


class ListUsersView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        organizations = Organization.objects.filter(users__in=[context_user])
        org_users = { organization: {"user": organization.users.all(), "profile": []} for organization in organizations }
        # retrieve the profile of each user and add to the org_user's related dictionary
        for org, users in org_users.items():
            for user in users['user']:
                profile = Profile.objects.filter(user=user).first()
                users['profile'].append(profile)
        # zip the profile and user together
        org_users = { org: tuple(zip(users['user'], users['profile'])) for org, users in org_users.items() }
        context['org_users'] = org_users
        context['context_user'] = context_user
        return context

    def post(self, request, *args, **kwargs):
        form = UserStatusForm(request.POST)
        if form.is_valid():
            user_id = request.POST.get('user_id')
            profile = get_object_or_404(Profile, user__id=user_id)
            profile.is_active = form.cleaned_data['is_active']
            profile.save()
            messages.success(request, 'User status updated successfully!')
        else:
            messages.error(request, 'Failed to update user status.')
        return redirect('user_management:list')


class RemoveUserView(LoginRequiredMixin, TemplateView):
    template_name = "user_management/confirm_remove_user.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = get_object_or_404(User, id=kwargs['pk'])
        context['user_to_delete'] = user
        return context

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs['pk'])
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('user_management:list')


@method_decorator(require_POST, name='dispatch')
class UpdateUserStatusView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        is_active = request.POST.get('is_active') == 'true'

        try:
            user = User.objects.get(id=user_id)
            user.profile.is_active = is_active
            user.profile.save()
            return redirect('user_management:list')
        except Exception as e:
            messages.error(request, f'Error updating user status')
            return redirect('user_management:list')
