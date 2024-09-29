#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: create_script_views.py
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
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.mm_scripts.forms import CustomScriptForm
from apps.mm_scripts.utils import CUSTOM_SCRIPT_CATEGORIES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateCustomScriptView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of new custom scripts.

    This view allows users to create custom scripts that can be utilized by their assistants. The view checks user permissions before allowing the creation of a new custom script.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the form for creating a custom script.
        post(self, request, *args, **kwargs): Processes the form submission to create a new custom script and associates it with the user.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = CustomScriptForm()
        context['CUSTOM_SCRIPT_CATEGORIES'] = CUSTOM_SCRIPT_CATEGORIES
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_SCRIPTS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_SCRIPTS):
            messages.error(self.request, "You do not have permission to add scripts.")
            return redirect('mm_scripts:list')
        ##############################

        form = CustomScriptForm(request.POST, request.FILES)
        if form.is_valid():
            custom_script = form.save(commit=False)
            custom_script.created_by_user = request.user
            # Handle dynamic fields
            categories = request.POST.getlist('categories')
            # Process step guide
            step_guide = request.POST.getlist('script_step_guide[]')
            custom_script.script_step_guide = step_guide
            # Save the image
            if request.FILES.get('script_picture'):
                custom_script.script_picture = request.FILES.get('script_picture')
            custom_script.categories = categories
            # Process script content
            script_content = request.POST.get('code_text', '')
            custom_script.script_content = script_content
            custom_script.save()
            print('[CreateCustomScriptView.post] Custom Script created successfully.')
            messages.success(request, "Custom Script created successfully!")
            return redirect('mm_scripts:list')
        else:
            messages.error(request, "There was an error creating the custom script.")

        return render(request, self.template_name, {
            'form': form, 'CUSTOM_SCRIPT_CATEGORIES': CUSTOM_SCRIPT_CATEGORIES,
        })
