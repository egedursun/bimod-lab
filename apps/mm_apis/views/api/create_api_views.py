#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: create_api_views.py
#  Last Modified: 2024-09-28 16:27:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:00:11
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
from apps.assistants.models import Assistant
from apps.mm_apis.forms import CustomAPIForm
from apps.mm_apis.utils import CUSTOM_API_CATEGORIES, CUSTOM_API_AUTHENTICATION_TYPES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CreateCustomAPIView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of new custom APIs.

    This view allows users to create custom APIs that can be integrated into their assistants. The view checks user
    permissions before allowing the creation of a new API.

    Methods: get_context_data(self, **kwargs): Prepares the context with the form and API categories. post(self,
    request, *args, **kwargs): Processes the form submission to create a new custom API and associates it with the
    user.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = CustomAPIForm()
        context['CUSTOM_API_CATEGORIES'] = CUSTOM_API_CATEGORIES
        context['CUSTOM_API_AUTHENTICATION_TYPES'] = CUSTOM_API_AUTHENTICATION_TYPES
        return context

    def post(self, request, *args, **kwargs):
        form = CustomAPIForm(request.POST, request.FILES)

        ##############################
        # PERMISSION CHECK FOR - ADD_APIS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_APIS):
            messages.error(self.request, "You do not have permission to add custom APIs.")
            return redirect('mm_apis:list')
        ##############################

        if form.is_valid():
            custom_api = form.save(commit=False)
            custom_api.created_by_user = request.user
            # Handle dynamic fields
            endpoints = {}
            endpoint_keys = [key for key in request.POST.keys() if key.startswith('endpoints[')]
            endpoint_indices = set(key.split('[')[1].split(']')[0] for key in endpoint_keys)
            for i in endpoint_indices:
                name = request.POST.get(f'endpoints[{i}][name]')
                if name:  # Only add if name is not empty
                    endpoint_data = {
                        'description': request.POST.get(f'endpoints[{i}][description]', ''),
                        'path': request.POST.get(f'endpoints[{i}][path]', ''),
                        'method': request.POST.get(f'endpoints[{i}][method]', ''),
                        'header_params': request.POST.getlist(f'endpoints[{i}][header_params][]'),
                        'path_params': request.POST.getlist(f'endpoints[{i}][path_params][]'),
                        'query_params': request.POST.getlist(f'endpoints[{i}][query_params][]'),
                        'body_params': request.POST.getlist(f'endpoints[{i}][body_params][]')
                    }
                    endpoints[name] = endpoint_data
            custom_api.endpoints = endpoints

            # Save the image
            if request.FILES.get('api_picture'):
                custom_api.api_picture = request.FILES.get('api_picture')
            custom_api.categories = request.POST.getlist('categories')
            custom_api.save()
            print('[CreateCustomAPIView.post] Custom API created successfully.')
            return redirect('mm_apis:list')
        return render(request, self.template_name, {'form': form, 'assistants': Assistant.objects.filter(
            organization__users__in=[request.user]
        )})
