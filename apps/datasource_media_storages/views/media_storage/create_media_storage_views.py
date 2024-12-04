#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_media_storage_views.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:48
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

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.assistants.models import Assistant

from apps.datasource_media_storages.models import (
    DataSourceMediaStorageConnection
)

from apps.datasource_media_storages.utils import (
    MEDIA_MANAGER_ITEM_TYPES
)

from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from config.settings import MAX_MEDIA_STORAGES_PER_ASSISTANT
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class MediaView_ManagerCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user

        try:
            user_orgs = Organization.objects.filter(
                users__in=[context_user]
            )

            context['assistants'] = Assistant.objects.filter(
                organization__in=user_orgs
            )

            context['media_categories'] = MEDIA_MANAGER_ITEM_TYPES
            context['user'] = context_user

        except Exception as e:
            logger.error(f"User: {context_user} - Media Storage - Create Error: {e}")
            messages.error(self.request, 'An error occurred while creating media storage.')

            return context

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_MEDIA_STORAGES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_MEDIA_STORAGES
        ):
            messages.error(self.request, "You do not have permission to create media storages.")
            return redirect('datasource_media_storages:list')
        ##############################

        name = request.POST.get('name')
        desc = request.POST.get('description')
        item_category = request.POST.get('media_category')
        agent_id = request.POST.get('assistant')

        try:
            agent = Assistant.objects.get(
                id=agent_id
            )

            n_media_storages = agent.datasourcemediastorageconnection_set.count()

            if n_media_storages > MAX_MEDIA_STORAGES_PER_ASSISTANT:
                messages.error(
                    request,
                    f'Assistant has reached the maximum number of media storage connections ({MAX_MEDIA_STORAGES_PER_ASSISTANT}).'
                )

                return redirect('datasource_media_storages:create')

            media_manager = DataSourceMediaStorageConnection.objects.create(
                name=name,
                description=desc,
                media_category=item_category,
                assistant=agent
            )

            media_manager.save()

            logger.info('Data Source Media Storage created successfully.')
            messages.success(request, 'Data Source Media Storage created successfully.')

            return redirect('datasource_media_storages:list')

        except Assistant.DoesNotExist:
            logger.error('Invalid assistant selected.')
            messages.error(request, 'Invalid assistant selected.')

            return redirect('datasource_media_storages:create')

        except Exception as e:
            logger.error(f'Error creating Data Source Media Storage: {e}')
            messages.error(request, f'Error creating Data Source Media Storage: {e}')

            return redirect('datasource_media_storages:create')
