#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_store_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
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

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.mm_functions.models import CustomFunction, CustomFunctionReference
from apps.mm_functions.utils import CUSTOM_FUNCTION_CATEGORIES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class CustomFunctionView_Store(LoginRequiredMixin, TemplateView):
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        search_query = self.request.GET.get('search', '')
        selected_categories = self.request.GET.getlist('categories')
        functions_list = CustomFunction.objects.filter(is_public=True)
        if search_query:
            functions_list = functions_list.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query))
        if selected_categories:
            functions_list = functions_list.filter(
                *[Q(categories__icontains=category) for category in selected_categories])

        function_agent_map = {
            function.id: Assistant.objects.exclude(customfunctionreference__custom_function=function)
            for function in functions_list
        }
        paginator = Paginator(functions_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['functions'] = page_obj.object_list
        context['total_functions'] = CustomFunction.objects.count()
        context['public_functions'] = CustomFunction.objects.filter(is_public=True).count()
        context['private_functions'] = CustomFunction.objects.filter(is_public=False).count()
        context['search_query'] = search_query
        context['selected_categories'] = selected_categories
        context['CUSTOM_FUNCTION_CATEGORIES'] = CUSTOM_FUNCTION_CATEGORIES
        context['function_assistant_map'] = function_agent_map
        logger.info(f"User: {self.request.user.id} is checking function store.")
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        agent_id = request.POST.get('assistant_id')

        ##############################
        # PERMISSION CHECK FOR - UPDATE_FUNCTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_FUNCTIONS):
            logger.error(f"You do not have permission to update custom functions.")
            messages.error(self.request, "You do not have permission to update custom functions.")
            return redirect('mm_functions:list')
        ##############################

        if action and action == "add" and agent_id:
            function_id = request.POST.get('function_id')
            if function_id:
                custom_function = CustomFunction.objects.get(id=function_id)
                agent = Assistant.objects.get(id=agent_id)
                CustomFunctionReference.objects.create(assistant=agent, custom_function=custom_function,
                                                       created_by_user=request.user)
                logger.info(f"Function '{custom_function.name}' assigned to assistant '{agent.name}'.")
                messages.success(request,
                                 f"Function '{custom_function.name}' assigned to assistant '{agent.name}'.")
        else:
            logger.error(f"Invalid input. Please try again.")
            messages.error(request, "Invalid input. Please try again.")
        return redirect('mm_functions:store')
