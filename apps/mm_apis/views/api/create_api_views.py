#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_api_views.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.mm_apis.forms import CustomAPIForm
from apps.mm_apis.utils import CATEGORIES_OF_CUSTOM_APIS, CUSTOM_API_AUTHENTICATION_TYPES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class CustomAPIView_Create(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = CustomAPIForm()
        context['CUSTOM_API_CATEGORIES'] = CATEGORIES_OF_CUSTOM_APIS
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
            endpoints = {}
            endpoint_keys = [key for key in request.POST.keys() if key.startswith('endpoints[')]
            endpoint_indices = set(key.split('[')[1].split(']')[0] for key in endpoint_keys)
            for i in endpoint_indices:
                name = request.POST.get(f'endpoints[{i}][name]')
                if name:
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
            if request.FILES.get('api_picture'):
                custom_api.api_picture = request.FILES.get('api_picture')
            custom_api.categories = request.POST.getlist('categories')
            custom_api.save()
            logger.info(f"Custom API was created by User: {self.request.user.id}.")
            return redirect('mm_apis:list')
        return render(request, self.template_name, {'form': form, 'assistants': Assistant.objects.filter(
            organization__users__in=[request.user])})
