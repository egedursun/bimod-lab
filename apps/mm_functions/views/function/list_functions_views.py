#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: list_functions_views.py
#  Last Modified: 2024-09-28 16:27:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:01:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_functions.models import CustomFunction
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListCustomFunctionsView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of custom functions created by users within the connected organizations.

    This view retrieves and displays all custom functions that are available to the current user, with support for searching and pagination.

    Methods:
        get_context_data(self, **kwargs): Retrieves the user's accessible custom functions and adds them to the context.
    """

    template_name = "mm_functions/functions/list_custom_functions.html"
    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_FUNCTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_FUNCTIONS):
            messages.error(self.request, "You do not have permission to list custom functions.")
            return context
        ##############################

        context_user = self.request.user
        connected_organizations = Organization.objects.filter(users__in=[context_user])
        users_of_connected_organizations = User.objects.filter(
            profile__user__in=[user for org in connected_organizations for user in org.users.all()])
        functions_list = CustomFunction.objects.filter(created_by_user__in=users_of_connected_organizations)
        search_query = self.request.GET.get('search', '')
        if search_query:
            functions_list = functions_list.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        paginator = Paginator(functions_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['functions'] = page_obj.object_list
        context['total_functions'] = CustomFunction.objects.count()
        context['public_functions'] = CustomFunction.objects.filter(is_public=True).count()
        context['private_functions'] = CustomFunction.objects.filter(is_public=False).count()
        context['search_query'] = search_query
        return context
