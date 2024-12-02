#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_file_system_views.py
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
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_file_systems.models import DataSourceFileSystem
from apps.datasource_file_systems.utils import DATASOURCE_FILE_SYSTEMS_OS_TYPES
from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_FILE_SYSTEMS_PER_ASSISTANT
from web_project import TemplateLayout


logger = logging.getLogger(__name__)


class FileSystemView_Create(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        orgs = context_user.organizations.filter(users__in=[context_user])
        context['assistants'] = Assistant.objects.filter(organization__in=orgs)
        context['os_choices'] = DATASOURCE_FILE_SYSTEMS_OS_TYPES
        context['user'] = context_user
        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_FILE_SYSTEMS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_FILE_SYSTEMS):
            messages.error(self.request, "You do not have permission to create a file system connection.")
            return redirect('datasource_file_systems:list')
        ##############################

        name = request.POST.get('name')
        description = request.POST.get('description')
        os_type = request.POST.get('os_type')
        agent_id = request.POST.get('assistant')
        host_url = request.POST.get('host_url')
        port = request.POST.get('port', 22)
        username = request.POST.get('username')
        password = request.POST.get('password')
        os_read_limit_tokens = request.POST.get('os_read_limit_tokens', 5_000)
        is_read_only = request.POST.get('is_read_only') == 'on'
        created_by_user = request.user

        try:
            agent = Assistant.objects.get(id=agent_id)

            # check the number of browser connections assistant has
            n_file_systems = agent.data_source_file_systems.count()
            if n_file_systems > MAX_FILE_SYSTEMS_PER_ASSISTANT:
                messages.error(request,
                               f'Assistant has reached the maximum number of file system connections ({MAX_FILE_SYSTEMS_PER_ASSISTANT}).')
                return redirect('datasource_file_systems:create')

            conn = DataSourceFileSystem.objects.create(
                name=name, description=description,
                os_type=os_type,
                assistant=agent,
                host_url=host_url,
                port=port,
                username=username,
                password=password,
                os_read_limit_tokens=os_read_limit_tokens,
                is_read_only=is_read_only,
                created_by_user=created_by_user
            )

            conn.save()

            logger.info(f"Data Source File System created successfully.")
            messages.success(request, 'Data Source File System created successfully.')
            return redirect('datasource_file_systems:list')

        except Assistant.DoesNotExist:
            logger.error(f'Invalid assistant selected.')
            messages.error(request, 'Invalid assistant selected.')
            return redirect('datasource_file_systems:create')

        except Exception as e:
            logger.error(f'Error creating Data Source File System: {e}')
            messages.error(request, f'Error creating Data Source File System: {e}')
            return redirect('datasource_file_systems:list')
