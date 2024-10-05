#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: function_store_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:37
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: function_store_views.py
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
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.mm_functions.models import CustomFunction, CustomFunctionReference
from apps.mm_functions.utils import CUSTOM_FUNCTION_CATEGORIES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class FunctionStoreView(LoginRequiredMixin, TemplateView):
    """
    Displays the function store where public functions are listed for users to integrate with their assistants.

    This view allows users to search, filter, and assign public functions to their assistants.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the available public functions, search query, and filters.
        post(self, request, *args, **kwargs): Processes the request to assign a selected function to an assistant.
    """

    template_name = "mm_functions/store/function_store.html"
    paginate_by = 10  # Adjust the number of items per page

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

        # for each of the functions, we must only offer the assistants that currently does not have a function
        # reference for that function
        function_assistant_map = {
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
        context['function_assistant_map'] = function_assistant_map
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        assistant_id = request.POST.get('assistant_id')

        ##############################
        # PERMISSION CHECK FOR - UPDATE_FUNCTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_FUNCTIONS):
            messages.error(self.request, "You do not have permission to update custom functions.")
            return redirect('mm_functions:list')
        ##############################

        if action and action == "add" and assistant_id:
            function_id = request.POST.get('function_id')
            if function_id:
                custom_function = CustomFunction.objects.get(id=function_id)
                assistant = Assistant.objects.get(id=assistant_id)
                CustomFunctionReference.objects.create(
                    assistant=assistant,
                    custom_function=custom_function,
                    created_by_user=request.user
                )
                print(
                    f"[FunctionStoreView.post] Function '{custom_function.name}' assigned to assistant '{assistant.name}'.")
                messages.success(request,
                                 f"Function '{custom_function.name}' assigned to assistant '{assistant.name}'.")
        else:
            messages.error(request, "Invalid input. Please try again.")

        return redirect('mm_functions:store')
