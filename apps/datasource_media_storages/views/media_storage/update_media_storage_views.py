#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: update_media_storage_views.py
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection
from apps.datasource_media_storages.utils import MEDIA_MANAGER_ITEM_TYPES
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class MediaView_ManagerUpdate(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        media_manager = get_object_or_404(DataSourceMediaStorageConnection, pk=kwargs['pk'])
        user_orgs = Organization.objects.filter(users__in=[context_user])
        context['assistants'] = Assistant.objects.filter(organization__in=user_orgs)
        context['media_categories'] = MEDIA_MANAGER_ITEM_TYPES
        context['user'] = context_user
        context['connection'] = media_manager
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - UPDATE_MEDIA_STORAGES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_MEDIA_STORAGES):
            messages.error(self.request, "You do not have permission to update media storages.")
            return redirect('datasource_media_storages:list')
        ##############################

        media_manager = get_object_or_404(DataSourceMediaStorageConnection, pk=kwargs['pk'])
        name = request.POST.get('name')
        desc = request.POST.get('description')
        manager_category = request.POST.get('media_category')
        agent_id = request.POST.get('assistant')

        try:
            agent = Assistant.objects.get(id=agent_id)
            media_manager.name = name
            media_manager.description = desc
            media_manager.media_category = manager_category
            media_manager.assistant = agent
            media_manager.save()
            messages.success(request, 'Data Source Media Storage updated successfully.')
            return redirect('datasource_media_storages:list')
        except Assistant.DoesNotExist:
            messages.error(request, 'Invalid assistant selected.')
            return redirect('datasource_media_storages:update', pk=media_manager.pk)
        except Exception as e:
            messages.error(request, f'Error updating Data Source Media Storage: {e}')
            return redirect('datasource_media_storages:update', pk=media_manager.pk)
