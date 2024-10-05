#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: update_file_system_views.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:45
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
#  File: update_file_system_views.py
#  Last Modified: 2024-09-28 00:53:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:41:09
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_file_systems.models import DataSourceFileSystem
from apps.datasource_file_systems.utils import DATASOURCE_FILE_SYSTEMS_OS_TYPES
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DataSourceFileSystemUpdateView(LoginRequiredMixin, TemplateView):
    """
    Handles updating an existing data source file system connection.

    This view allows users with the appropriate permissions to modify a file system connection's attributes. It also handles the form submission and validation for updating the connection.

    Attributes:
        template_name (str): The template used to render the file system update form.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current file system connection details and adds them to the context, along with other relevant data such as available assistants and OS choices.
        post(self, request, *args, **kwargs): Handles form submission for updating the file system connection, including permission checks and validation.
    """

    template_name = 'datasource_file_systems/update_datasource_file_system.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        organizations = context_user.organizations.filter(users__in=[context_user])
        context['assistants'] = Assistant.objects.filter(organization__in=organizations)
        context['os_choices'] = DATASOURCE_FILE_SYSTEMS_OS_TYPES
        context['user'] = context_user
        try:
            connection = DataSourceFileSystem.objects.get(pk=kwargs['pk'])
            context['connection'] = connection
        except DataSourceFileSystem.DoesNotExist:
            messages.error(self.request, 'Data Source File System not found.')
            return redirect('datasource_file_systems:list')
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - UPDATE_FILE_SYSTEMS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_FILE_SYSTEMS):
            messages.error(self.request, "You do not have permission to update a file system connection.")
            return redirect('datasource_file_systems:list')
        ##############################

        try:
            connection = get_object_or_404(DataSourceFileSystem, pk=kwargs['pk'])
        except DataSourceFileSystem.DoesNotExist:
            messages.error(request, 'Data Source File System not found.')
            return redirect('datasource_file_systems:list')

        connection.name = request.POST.get('name')
        connection.description = request.POST.get('description')
        connection.os_type = request.POST.get('os_type')
        assistant_id = request.POST.get('assistant')
        connection.host_url = request.POST.get('host_url')
        connection.port = request.POST.get('port', 22)
        connection.username = request.POST.get('username')
        connection.password = request.POST.get('password')
        connection.os_read_limit_tokens = request.POST.get('os_read_limit_tokens', 5_000)
        connection.is_read_only = request.POST.get('is_read_only') == 'on'

        try:
            assistant = Assistant.objects.get(id=assistant_id)
            connection.assistant = assistant
        except Assistant.DoesNotExist:
            messages.error(request, 'Invalid assistant selected.')
            return redirect('datasource_file_systems:update', kwargs={'pk': kwargs['pk']})

        try:
            connection.save()
            messages.success(request, 'Data Source File System updated successfully.')
            print('[DataSourceFileSystemUpdateView.post] Data Source File System updated successfully.')
            return redirect('datasource_file_systems:list')
        except Exception as e:
            messages.error(request, f'Error updating Data Source File System: {e}')
            return redirect('datasource_file_systems:update', kwargs={'pk': kwargs['pk']})
