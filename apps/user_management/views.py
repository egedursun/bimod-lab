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
from apps.user_permissions.models import PermissionNames, UserPermission
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
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - USER/CREATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_USERS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add new users."}
            return self.render_to_response(context)
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

        return redirect('user_management:list')


class AddUserToOrganizationView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context_user_organizations = Organization.objects.filter(users__in=[self.request.user])
        context_users_users = context_user_organizations.values_list('users', flat=True)
        context['users'] = User.objects.exclude(id__in=context_users_users)
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - USER/ADD TO ORGANIZATION
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if (PermissionNames.UPDATE_USERS not in user_permissions and
            PermissionNames.UPDATE_ORGANIZATIONS not in user_permissions):
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to add users to organizations."}
            return self.render_to_response(context)
        ##############################

        user = request.POST.get('user')
        organization_id = request.POST.get('organization')

        try:
            user = User.objects.get(id=user)
            organization = Organization.objects.get(id=organization_id)
            if user in organization.users.all():
                messages.error(request, 'User is already a member of this organization.')
            else:
                organization.users.add(user)
                messages.success(request, 'User added to organization successfully!')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
        except Organization.DoesNotExist:
            messages.error(request, 'Organization does not exist.')
        except Exception as e:
            messages.error(request, f'Error adding user to organization: {str(e)}')

        return redirect('user_management:add_user_to_organization')


class ListUsersView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - USER/LIST
        ##############################
        # For now, we will allow all users to view the list of users
        ##############################

        organizations = Organization.objects.filter(users__in=[context_user])
        org_users = {organization: {"user": organization.users.all(), "profile": []} for organization in organizations}
        # retrieve the profile of each user and add to the org_user's related dictionary
        for org, users in org_users.items():
            for user in users['user']:
                profile = Profile.objects.filter(user=user).first()
                users['profile'].append(profile)
        # zip the profile and user together
        org_users = {org: tuple(zip(users['user'], users['profile'])) for org, users in org_users.items()}
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

            # Update all permissions associated with the user, and set them to whatever is_active is
            user = profile.user
            user_permissions = user.permissions.all()
            for user_permission in user_permissions:
                user_permission.is_active = profile.is_active
                user_permission.save()

            messages.success(request, 'User status updated successfully!')
        else:
            messages.error(request, 'Failed to update user status.')
        return redirect('user_management:list')


class RemoveUserFromOrganizationView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = get_object_or_404(User, id=kwargs['pk'])
        print(user)
        organization = get_object_or_404(Organization, id=kwargs['org_id'])
        context['user_to_remove'] = user
        context['organization'] = organization
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - USER/REMOVE FROM ORGANIZATION
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_USERS not in user_permissions:
            messages.error(request, "You do not have permission to remove users from organizations.")
            return redirect('user_management:list')
        ##############################

        user = get_object_or_404(User, id=kwargs['pk'])
        organization = get_object_or_404(Organization, id=kwargs['org_id'])
        organization.users.remove(user)
        organization.save()

        messages.success(request, f'User removed from {organization.name} successfully.')
        return redirect('user_management:list')


class RemoveUserView(LoginRequiredMixin, TemplateView):
    template_name = "user_management/confirm_remove_user.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = get_object_or_404(User, id=kwargs['pk'])
        context['user_to_delete'] = user
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - USER/DELETE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_USERS not in user_permissions:
            messages.error(request, "You do not have permission to delete users.")
            return redirect('user_management:list')
        ##############################

        user = get_object_or_404(User, id=kwargs['pk'])

        # remove the user from all organizations
        organizations = Organization.objects.filter(users__in=[user])
        for organization in organizations:
            organization.users.remove(user)
            organization.save()

        user.delete()
        # remove the user from all organizations
        messages.success(request, 'User deleted successfully.')
        return redirect('user_management:list')


@method_decorator(require_POST, name='dispatch')
class UpdateUserStatusView(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        user_id = request.POST.get('user_id')
        is_active = request.POST.get('is_active') == 'true'

        ##############################
        # PERMISSION CHECK FOR - USER/UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_USERS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to update user status."}
            return self.render_to_response(context)
        ##############################

        try:
            user = User.objects.get(id=user_id)
            user.profile.is_active = is_active
            user.profile.save()
            return redirect('user_management:list')
        except Exception as e:
            messages.error(request, f'Error updating user status')
            return redirect('user_management:list')
