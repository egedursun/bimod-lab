#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: api_store_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
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
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.mm_apis.models import CustomAPI, CustomAPIReference
from apps.mm_apis.utils import CATEGORIES_OF_CUSTOM_APIS
from apps.user_permissions.models import UserPermission
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CustomAPIView_Store(LoginRequiredMixin, TemplateView):
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        search_query = self.request.GET.get('search', '')
        selected_categories = self.request.GET.getlist('categories')
        apis_list = CustomAPI.objects.filter(is_public=True)
        if search_query:
            apis_list = apis_list.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        if selected_categories:
            apis_list = apis_list.filter(*[Q(categories__icontains=category) for category in selected_categories])

        api_assistant_map = {
            api.id: Assistant.objects.exclude(customapireference__custom_api=api) for api in apis_list
        }

        paginator = Paginator(apis_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['apis'] = page_obj.object_list
        context['total_apis'] = CustomAPI.objects.count()
        context['public_apis'] = CustomAPI.objects.filter(is_public=True).count()
        context['private_apis'] = CustomAPI.objects.filter(is_public=False).count()
        context['search_query'] = search_query
        context['selected_categories'] = selected_categories
        context['CUSTOM_API_CATEGORIES'] = CATEGORIES_OF_CUSTOM_APIS
        context['api_assistant_map'] = api_assistant_map
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_APIS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_APIS):
            messages.error(self.request, "You do not have permission to update custom APIs.")
            return redirect('mm_apis:store')
        ##############################

        action = request.POST.get('action')
        agent_id = request.POST.get('assistant_id')
        if action and action == "add" and agent_id:
            api_id = request.POST.get('api_id')
            if api_id:
                custom_api = CustomAPI.objects.get(id=api_id)
                agent = Assistant.objects.get(id=agent_id)
                CustomAPIReference.objects.create(assistant=agent, custom_api=custom_api, created_by_user=request.user)
                messages.success(request, f"API '{custom_api.name}' assigned to assistant '{agent.name}'.")
        else:
            messages.error(request, "Invalid input. Please try again.")
        return redirect('mm_apis:store')
