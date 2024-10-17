#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_video_generator_connection_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:45
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
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.core.video_generation.utils import VIDEO_GENERATOR_PROVIDER_TYPES
from apps.assistants.models import Assistant
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from apps.video_generations.models import VideoGeneratorConnection
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class VideoGeneratorView_Update(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        pk = self.kwargs.get('pk')
        video_generator_connection = get_object_or_404(VideoGeneratorConnection, pk=pk)
        context['video_generator_connection'] = video_generator_connection
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        context['assistants'] = Assistant.objects.filter(organization__in=context['organizations'])
        context['provider_choices'] = VIDEO_GENERATOR_PROVIDER_TYPES
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_VIDEO_GENERATOR_CONNECTIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_VIDEO_GENERATOR_CONNECTIONS):
            messages.error(self.request, "You do not have permission to update video generator connections.")
            return redirect('video_generations:list')
        ##############################

        pk = self.kwargs.get('pk')
        video_generator_connection = get_object_or_404(VideoGeneratorConnection, pk=pk)
        org_id = request.POST.get('organization')
        agent_id = request.POST.get('assistant')
        name = request.POST.get('name')
        description = request.POST.get('description')
        provider = request.POST.get('provider')
        provider_api_key = request.POST.get('provider_api_key')

        errors = {}
        if not org_id:
            errors['organization'] = 'Organization is required.'
        if not agent_id:
            errors['assistant'] = 'Assistant is required.'
        if not name:
            errors['name'] = 'Name is required.'
        if not description:
            errors['description'] = 'Description is required.'
        if not provider:
            errors['provider'] = 'Provider is required.'
        if not provider_api_key:
            errors['provider_api_key'] = 'Provider API Key is required.'

        if errors:
            context = self.get_context_data()
            context['error_messages'] = errors
            logger.error(f"Error updating the Video Generator Connection. Errors: {errors}")
            return render(request, self.template_name, context)

        orgg = None
        agent = None
        try:
            orgg = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            logger.error(f"Organization with ID {org_id} does not exist.")
            errors['organization'] = 'Selected organization does not exist.'
        try:
            agent = Assistant.objects.get(id=agent_id)
        except Assistant.DoesNotExist:
            logger.error(f"Assistant with ID {agent_id} does not exist.")
            errors['assistant'] = 'Selected assistant does not exist.'
        if errors:
            context = self.get_context_data()
            context['error_messages'] = errors
            logger.error(f"Error updating the Video Generator Connection. Errors: {errors}")
            return render(request, self.template_name, context)

        if orgg is None:
            errors['organization'] = 'Selected organization does not exist.'
            logger.error(f"Error updating the Video Generator Connection. Errors: {errors}")
        if agent is None:
            errors['assistant'] = 'Selected assistant does not exist.'
            logger.error(f"Error updating the Video Generator Connection. Errors: {errors}")
        if errors:
            context = self.get_context_data()
            context['error_messages'] = errors
            logger.error(f"Error updating the Video Generator Connection. Errors: {errors}")
            return render(request, self.template_name, context)

        video_generator_connection.organization = orgg
        video_generator_connection.assistant = agent
        video_generator_connection.name = name
        video_generator_connection.description = description
        video_generator_connection.provider = provider
        video_generator_connection.provider_api_key = provider_api_key
        video_generator_connection.save()
        logger.info(f"Video Generator Connection updated by User: {self.request.user.id}.")
        messages.success(request, 'Video Generator Connection updated successfully.')
        return redirect('video_generations:list')
