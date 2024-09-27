from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


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
