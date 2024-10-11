#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: list_scripts_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.mm_scripts.models import CustomScript
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CustomScriptView_List(LoginRequiredMixin, TemplateView):
    paginate_by = 10

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
        conn_orgs = Organization.objects.filter(users__in=[context_user])
        users_of_conn_orgs = User.objects.filter(profile__user__in=[
            user for org in conn_orgs for user in org.users.all()])
        scripts_list = CustomScript.objects.filter(created_by_user__in=users_of_conn_orgs)
        search_query = self.request.GET.get('search', '')
        if search_query:
            scripts_list = scripts_list.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query))

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
