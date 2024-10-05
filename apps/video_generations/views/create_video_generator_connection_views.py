#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: create_video_generator_connection_views.py
#  Last Modified: 2024-10-01 22:54:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:43
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
#  File: create_video_generator_connection_views.py
#  Last Modified: 2024-10-01 17:06:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-10-01 17:06:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@bimod.io.
#
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps._services.video_generation.utils import VIDEO_GENERATOR_PROVIDER_TYPES
from apps.assistants.models import Assistant
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from apps.video_generations.models import VideoGeneratorConnection
from web_project import TemplateLayout


class CreateVideoGeneratorConnectionView(LoginRequiredMixin, TemplateView):
    template_name = 'video_generations/connection/create_video_generator_connection.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(
            users__in=[self.request.user]
        )
        context['assistants'] = Assistant.objects.filter(
            organization__in=context['organizations']
        )
        context['provider_choices'] = VIDEO_GENERATOR_PROVIDER_TYPES
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - CREATE_VIDEO_GENERATOR_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_VIDEO_GENERATOR_CONNECTIONS):
            messages.error(self.request, "You do not have permission to create video generator connections.")
            return redirect('video_generations:list')
        ##############################

        # Retrieve form data
        organization_id = request.POST.get('organization')
        assistant_id = request.POST.get('assistant')
        name = request.POST.get('name')
        description = request.POST.get('description')
        provider = request.POST.get('provider')
        provider_api_key = request.POST.get('provider_api_key')

        # Validate form data
        errors = {}
        if not organization_id:
            errors['organization'] = 'Organization is required.'
        if not assistant_id:
            errors['assistant'] = 'Assistant is required.'
        if not name:
            errors['name'] = 'Name is required.'
        if not description:
            errors['description'] = 'Description is required.'
        if not provider:
            errors['provider'] = 'Provider is required.'
        if not provider_api_key:
            errors['provider_api_key'] = 'Provider API Key is required.'

        # Check for errors
        if errors:
            context = self.get_context_data()
            context['error_messages'] = errors
            return render(request, self.template_name, context)

        # Get organization and assistant instances
        organization = None
        assistant = None
        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            errors['organization'] = 'Selected organization does not exist.'
        try:
            assistant = Assistant.objects.get(id=assistant_id)
        except Assistant.DoesNotExist:
            errors['assistant'] = 'Selected assistant does not exist.'
        if errors:
            context = self.get_context_data()
            context['error_messages'] = errors
            return render(request, self.template_name, context)

        if organization is None:
            errors['organization'] = 'Selected organization does not exist.'
        if assistant is None:
            errors['assistant'] = 'Selected assistant does not exist.'
        if errors:
            context = self.get_context_data()
            context['error_messages'] = errors
            return render(request, self.template_name, context)

        # Create VideoGeneratorConnection instance
        video_generator_connection = VideoGeneratorConnection(
            organization=organization,
            assistant=assistant,
            created_by_user=request.user,
            name=name,
            description=description,
            provider=provider,
            provider_api_key=provider_api_key
        )
        video_generator_connection.save()

        # Success message and redirect
        messages.success(request, 'Video Generator Connection created successfully.')
        return redirect('video_generations:list')
