"""
View to handle the creation of new users.

This view allows administrators to create new users by providing details like username, email, password, and more. It also sends a verification and invitation email to the newly created user.

Methods:
    get_context_data(self, **kwargs): Prepares the context with a list of organizations to which the user can be added.
    post(self, request, *args, **kwargs): Handles the user creation logic, including sending verification and invitation emails.
"""

import uuid

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_management.forms import UserStatusForm
from apps.user_permissions.models import PermissionNames, UserPermission
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


class AddUserToOrganizationView(LoginRequiredMixin, TemplateView):
    """
    View to add an existing user to an organization.

    This view allows administrators to add existing users (sub-users) to an organization that the administrator belongs to.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the list of sub-users and organizations the user can manage.
        post(self, request, *args, **kwargs): Handles the logic to add a user to the selected organization.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        context_sub_users = context_user.profile.sub_users.all()
        context['users'] = context_sub_users
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - CONNECT_USER_TO_ORGANIZATION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CONNECT_USER_TO_ORGANIZATION):
            messages.error(self.request, "You do not have permission to connect users to organizations.")
            return redirect('user_management:list')
        ##############################

        user = request.POST.get('user')
        organization_id = request.POST.get('organization')
        try:
            user = User.objects.get(id=user)
            organization = Organization.objects.get(id=organization_id)
            if user in organization.users.all():
                print('[AddUserToOrganizationView.post] User is already a member of this organization.')
                messages.error(request, 'User is already a member of this organization.')
            else:
                organization.users.add(user)
                print('[AddUserToOrganizationView.post] User added to organization successfully!')
                messages.success(request, 'User added to organization successfully!')
        except User.DoesNotExist:
            print('[AddUserToOrganizationView.post] User does not exist.')
            messages.error(request, 'User does not exist.')
        except Organization.DoesNotExist:
            print('[AddUserToOrganizationView.post] Organization does not exist.')
            messages.error(request, 'Organization does not exist.')
        except Exception as e:
            print(f'[AddUserToOrganizationView.post] Error adding user to organization: {str(e)}')
            messages.error(request, f'Error adding user to organization: {str(e)}')
        return redirect('user_management:add_user_to_organization')


class ListUsersView(LoginRequiredMixin, TemplateView):
    """
    View to list users associated with the logged-in user's organizations.

    This view displays a paginated list of users who are part of the organizations that the logged-in user belongs to. It also allows for updating user statuses.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the list of users grouped by organization.
        post(self, request, *args, **kwargs): Handles the logic to update the status (active/inactive) of a user.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_USERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_USERS):
            messages.error(self.request, "You do not have permission to list users.")
            return context
        ##############################

        context_user = self.request.user
        organizations = Organization.objects.filter(users__in=[context_user])
        search_query = self.request.GET.get('search', '')
        page_number = self.request.GET.get('page', 1)

        org_users = {}
        for organization in organizations:
            users = organization.users.all()
            if search_query:
                users = users.filter(
                    Q(username__icontains=search_query) | Q(email__icontains=search_query) |
                    Q(profile__first_name__icontains=search_query) | Q(profile__last_name__icontains=search_query)
                )
            paginator = Paginator(users, 10)  # Show 10 users per page
            page_obj = paginator.get_page(page_number)
            user_profiles = [(user, Profile.objects.filter(user=user).first()) for user in page_obj]
            org_users[organization] = {'page_obj': page_obj, 'user_profiles': user_profiles, 'search_query': search_query}
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
            print('[ListUsersView.post] User status updated successfully.')
            messages.success(request, 'User status updated successfully!')
        else:
            messages.error(request, 'Failed to update user status.')
        return redirect('user_management:list')


class RemoveUserFromOrganizationView(TemplateView, LoginRequiredMixin):
    """
    View to remove a user from a specific organization.

    This view allows administrators to remove a user from a particular organization. The user will no longer be associated with that organization.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with details of the user and organization to confirm the removal.
        post(self, request, *args, **kwargs): Handles the logic to remove the user from the specified organization.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = get_object_or_404(User, id=kwargs['pk'])
        organization = get_object_or_404(Organization, id=kwargs['org_id'])
        context['user_to_remove'] = user
        context['organization'] = organization
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - REMOVE_USER_FROM_ORGANIZATION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_USER_FROM_ORGANIZATION):
            messages.error(self.request, "You do not have permission to remove users from organizations.")
            return redirect('user_management:list')
        ##############################

        user = get_object_or_404(User, id=kwargs['pk'])
        organization = get_object_or_404(Organization, id=kwargs['org_id'])
        organization.users.remove(user)
        organization.save()
        print('[RemoveUserFromOrganizationView.post] User removed from organization successfully.')
        messages.success(request, f'User removed from {organization.name} successfully.')
        return redirect('user_management:list')


class RemoveUserFromAllOrganizationsView(TemplateView, LoginRequiredMixin):
    """
    View to remove a user from all organizations they belong to.

    This view allows administrators to remove a user from all organizations they are currently a member of, effectively disassociating them from all organizations.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with details of the user to confirm the removal from all organizations.
        post(self, request, *args, **kwargs): Handles the logic to remove the user from all organizations.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = get_object_or_404(User, id=kwargs['pk'])
        context['user_to_remove'] = user
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - REMOVE_USER_FROM_ORGANIZATION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_USER_FROM_ORGANIZATION):
            messages.error(self.request, "You do not have permission to remove users from organizations.")
            return redirect('user_management:list')
        ##############################

        user = get_object_or_404(User, id=kwargs['pk'])
        organizations = Organization.objects.filter(users__in=[user])
        for organization in organizations:
            organization.users.remove(user)
            organization.save()
        messages.success(request, f'User removed from all organizations successfully.')
        return redirect('user_management:list')


class RemoveUserView(LoginRequiredMixin, TemplateView):
    """
    View to delete a user from the system.

    This view allows administrators to permanently delete a user. The user will be removed from all associated organizations before deletion.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with details of the user to confirm the deletion.
        post(self, request, *args, **kwargs): Handles the logic to delete the user and remove them from all organizations.
    """

    template_name = "user_management/users/confirm_remove_user.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = get_object_or_404(User, id=kwargs['pk'])
        context['user_to_delete'] = user
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_USERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_USERS):
            messages.error(self.request, "You do not have permission to delete user accounts.")
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
        print('[RemoveUserView.post] User deleted successfully.')
        messages.success(request, 'User deleted successfully.')
        return redirect('user_management:list')


@method_decorator(require_POST, name='dispatch')
class UpdateUserStatusView(LoginRequiredMixin, TemplateView):
    """
    View to update the active status of a user.

    This view allows administrators to activate or deactivate a user. The user's active status in all associated permissions is also updated accordingly.

    Methods:
        post(self, request, *args, **kwargs): Handles the logic to update the user's active status.
    """

    def post(self, request, *args, **kwargs):
        context_user = self.request.user
        user_id = request.POST.get('user_id')
        is_active = request.POST.get('is_active') == 'true'

        ##############################
        # PERMISSION CHECK FOR - UPDATE_USERS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_USERS):
            messages.error(self.request, "You do not have permission to update/modify user accounts.")
            return redirect('user_management:list')
        ##############################

        try:
            user = User.objects.get(id=user_id)
            user.profile.is_active = is_active
            user.profile.save()
            return redirect('user_management:list')
        except Exception as e:
            print(f'[UpdateUserStatusView.post] Error updating user status: {str(e)}')
            messages.error(request, f'Error updating user status')
            return redirect('user_management:list')
