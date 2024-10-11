#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: update_file_system_views.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_file_systems.models import DataSourceFileSystem
from apps.datasource_file_systems.utils import DATASOURCE_FILE_SYSTEMS_OS_TYPES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class FileSystemView_Update(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        orgs = context_user.organizations.filter(users__in=[context_user])
        context['assistants'] = Assistant.objects.filter(organization__in=orgs)
        context['os_choices'] = DATASOURCE_FILE_SYSTEMS_OS_TYPES
        context['user'] = context_user
        try:
            conn = DataSourceFileSystem.objects.get(pk=kwargs['pk'])
            context['connection'] = conn
        except DataSourceFileSystem.DoesNotExist:
            messages.error(self.request, 'Data Source File System not found.')
            return redirect('datasource_file_systems:list')
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - UPDATE_FILE_SYSTEMS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_FILE_SYSTEMS):
            messages.error(self.request, "You do not have permission to update a file system connection.")
            return redirect('datasource_file_systems:list')
        ##############################

        try:
            c = get_object_or_404(DataSourceFileSystem, pk=kwargs['pk'])
        except DataSourceFileSystem.DoesNotExist:
            messages.error(request, 'Data Source File System not found.')
            return redirect('datasource_file_systems:list')

        c.name = request.POST.get('name')
        c.description = request.POST.get('description')
        c.os_type = request.POST.get('os_type')
        assistant_id = request.POST.get('assistant')
        c.host_url = request.POST.get('host_url')
        c.port = request.POST.get('port', 22)
        c.username = request.POST.get('username')
        c.password = request.POST.get('password')
        c.os_read_limit_tokens = request.POST.get('os_read_limit_tokens', 5_000)
        c.is_read_only = request.POST.get('is_read_only') == 'on'

        try:
            agent = Assistant.objects.get(id=assistant_id)
            c.assistant = agent
        except Assistant.DoesNotExist:
            messages.error(request, 'Invalid assistant selected.')
            return redirect('datasource_file_systems:update', kwargs={'pk': kwargs['pk']})

        try:
            c.save()
            messages.success(request, 'Data Source File System updated successfully.')
            return redirect('datasource_file_systems:list')
        except Exception as e:
            messages.error(request, f'Error updating Data Source File System: {e}')
            return redirect('datasource_file_systems:update', kwargs={'pk': kwargs['pk']})
