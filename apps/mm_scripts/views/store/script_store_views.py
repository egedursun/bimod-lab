#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: script_store_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
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
#  File: script_store_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:03:36
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
from apps.mm_scripts.models import CustomScript, CustomScriptReference
from apps.mm_scripts.utils import CUSTOM_SCRIPT_CATEGORIES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ScriptStoreView(LoginRequiredMixin, TemplateView):
    """
    Displays the script store, where users can browse and add public custom scripts.

    This view allows users to search, filter, and view public custom scripts in the store. Users can add these scripts to their assistants, provided they have the necessary permissions.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with data about the available public custom scripts.
        post(self, request, *args, **kwargs): Processes the form submission to add selected scripts to the user's assistants.
    """

    paginate_by = 10  # Adjust the number of items per page

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        search_query = self.request.GET.get('search', '')
        selected_categories = self.request.GET.getlist('categories')
        scripts_list = CustomScript.objects.filter(is_public=True)
        if search_query:
            scripts_list = scripts_list.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query))
        if selected_categories:
            scripts_list = scripts_list.filter(
                *[Q(categories__icontains=category) for category in selected_categories])
        # for each of the scripts, we must only offer the assistants that currently do not have a script
        # reference for that script
        script_assistant_map = {
            script.id: Assistant.objects.exclude(customscriptreference__custom_script=script)
            for script in scripts_list
        }
        paginator = Paginator(scripts_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['scripts'] = page_obj.object_list
        context['total_scripts'] = CustomScript.objects.count()
        context['public_scripts'] = CustomScript.objects.filter(is_public=True).count()
        context['private_scripts'] = CustomScript.objects.filter(is_public=False).count()
        context['CUSTOM_SCRIPT_CATEGORIES'] = CUSTOM_SCRIPT_CATEGORIES
        context['search_query'] = search_query
        context['selected_categories'] = selected_categories
        context['script_assistant_map'] = script_assistant_map
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_SCRIPTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_SCRIPTS):
            messages.error(self.request, "You do not have permission to update scripts.")
            return redirect('mm_scripts:list')
        ##############################

        action = request.POST.get('action')
        assistant_id = request.POST.get('assistant_id')
        if action and action == "add" and assistant_id:
            script_id = request.POST.get('script_id')
            if script_id:
                custom_script = CustomScript.objects.get(id=script_id)
                assistant = Assistant.objects.get(id=assistant_id)
                CustomScriptReference.objects.create(
                    assistant=assistant, custom_script=custom_script, created_by_user=request.user
                )
                print(f"Script '{custom_script.name}' assigned to assistant '{assistant.name}'.")
                messages.success(request, f"Script '{custom_script.name}' assigned to assistant '{assistant.name}'.")
        else:
            messages.error(request, "Invalid input. Please try again.")
        return redirect('mm_scripts:store')
