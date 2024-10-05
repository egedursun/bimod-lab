#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: create_function_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.mm_functions.forms import CustomFunctionForm
from apps.mm_functions.utils import CUSTOM_FUNCTION_CATEGORIES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateCustomFunctionView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of new custom functions.

    This view allows users to create custom functions that can be integrated into their assistants. The view checks user permissions before allowing the creation of a new function.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the form and function categories.
        post(self, request, *args, **kwargs): Processes the form submission to create a new custom function and associates it with the user.
    """

    template_name = "mm_functions/functions/create_custom_function.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = CustomFunctionForm()
        context['CUSTOM_FUNCTION_CATEGORIES'] = CUSTOM_FUNCTION_CATEGORIES
        return context

    def post(self, request, *args, **kwargs):
        form = CustomFunctionForm(request.POST, request.FILES)

        ##############################
        # PERMISSION CHECK FOR - ADD_FUNCTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_FUNCTIONS):
            messages.error(self.request, "You do not have permission to add custom functions.")
            return redirect('mm_functions:list')
        ##############################

        if form.is_valid():
            custom_function = form.save(commit=False)
            custom_function.created_by_user = request.user

            # Handle dynamic fields
            packages = []
            for name, version in zip(request.POST.getlist('packages[][name]'),
                                     request.POST.getlist('packages[][version]')):
                if name:  # Only add if name is not empty
                    packages.append({'name': name, 'version': version})
            custom_function.packages = packages
            categories = request.POST.getlist('categories')

            # Process input fields
            input_field_names = request.POST.getlist('input_fields[][name]')
            input_field_descriptions = request.POST.getlist('input_fields[][description]')
            input_field_types = request.POST.getlist('input_fields[][type]')
            input_field_requireds = request.POST.getlist('input_fields[][required]')

            input_fields = []
            for i in range(len(input_field_names)):
                input_fields.append({
                    'name': input_field_names[i] if i < len(input_field_names) else '',
                    'description': input_field_descriptions[i] if i < len(input_field_descriptions) else '',
                    'type': input_field_types[i] if i < len(input_field_types) else '',
                    'required': bool(input_field_requireds[i]) if i < len(input_field_requireds) else False
                })
            custom_function.input_fields = input_fields

            # Process output fields
            output_field_names = request.POST.getlist('output_fields[][name]')
            output_field_descriptions = request.POST.getlist('output_fields[][description]')
            output_field_types = request.POST.getlist('output_fields[][type]')

            output_fields = []
            for i in range(len(output_field_names)):
                output_fields.append({
                    'name': output_field_names[i] if i < len(output_field_names) else '',
                    'description': output_field_descriptions[i] if i < len(output_field_descriptions) else '',
                    'type': output_field_types[i] if i < len(output_field_types) else ''
                })
            custom_function.output_fields = output_fields

            # Process secrets fields
            secret_field_names = request.POST.getlist('secrets[][name]')
            secret_field_keys = request.POST.getlist('secrets[][key]')

            secrets = []
            for i in range(len(secret_field_names)):
                secrets.append({
                    'name': secret_field_names[i] if i < len(secret_field_names) else '',
                    'key': secret_field_keys[i] if i < len(secret_field_keys) else ''
                })
            custom_function.secrets = secrets

            # Save the image
            if request.FILES.get('function_picture'):
                custom_function.function_picture = request.FILES.get('function_picture')

            custom_function.categories = categories
            custom_function.save()
            print('[CreateCustomFunctionView.post] Custom Function created successfully.')
            return redirect('mm_functions:list')
        return render(request, self.template_name, {'form': form,
                                                    'assistants': Assistant.objects.filter(
                                                        organization__users__in=[request.user]
                                                    )})
