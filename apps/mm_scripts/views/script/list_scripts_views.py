from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_scripts.models import CustomScript
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


class ListCustomScriptsView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of custom scripts associated with the user's organization.

    This view retrieves and displays all custom scripts that are available to the current user, with support for searching and pagination.

    Methods:
        get_context_data(self, **kwargs): Retrieves the user's accessible custom scripts and adds them to the context.
    """

    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_SCRIPTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_SCRIPTS):
            messages.error(self.request, "You do not have permission to list scripts.")
            return context
        ##############################

        context_user = self.request.user
        connected_organizations = Organization.objects.filter(users__in=[context_user])
        users_of_connected_organizations = User.objects.filter(
            profile__user__in=[user for org in connected_organizations for user in org.users.all()])
        scripts_list = CustomScript.objects.filter(created_by_user__in=users_of_connected_organizations)
        search_query = self.request.GET.get('search', '')
        if search_query:
            scripts_list = scripts_list.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        paginator = Paginator(scripts_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['scripts'] = page_obj.object_list
        context['total_scripts'] = CustomScript.objects.count()
        context['public_scripts'] = CustomScript.objects.filter(is_public=True).count()
        context['private_scripts'] = CustomScript.objects.filter(is_public=False).count()
        context['search_query'] = search_query
        return context
