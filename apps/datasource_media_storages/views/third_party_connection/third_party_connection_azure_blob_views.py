#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: third_party_connection_azure_blob_views.py
#  Last Modified: 2024-12-05 16:06:24
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-05 16:06:25
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.assistants.models import Assistant

from apps.core.media_managers.media_manager_execution_handler import (
    MediaManager
)

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_media_storages.models import (
    DataSourceMediaStorageConnection
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class MediaView_ThirdPartyConnection_AzureBlob(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        org_assistants = Assistant.objects.filter(
            organization__in=user_orgs
        )

        media_storages = DataSourceMediaStorageConnection.objects.filter(
            assistant__in=org_assistants
        )

        context['organizations'] = user_orgs
        context['assistants'] = org_assistants
        context['media_storages'] = media_storages

        return context

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - ADD_STORAGE_FILES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_STORAGE_FILES
        ):
            messages.error(self.request, "You do not have permission to add media files.")
            return redirect('datasource_media_storages:connect_azure_blob')
        ##############################

        try:

            account_name = request.POST.get('account_name')
            account_key = request.POST.get('account_key')
            container_name = request.POST.get('container_name')

            prefix = request.POST.get('prefix')
            media_storage_id = request.POST.get('media_storage_id')

            media_storage = DataSourceMediaStorageConnection.objects.get(
                id=media_storage_id
            )

            if media_storage is None:
                logger.error(f"Media Storage with ID '{media_storage_id}' not found.")
                messages.error(request, "Media Storage not found.")

                return redirect('datasource_media_storages:connect_azure_blob')

            success = MediaManager.copy_azure_bucket_into_storage(
                media_storage_id=media_storage_id,
                account_name=account_name,
                account_key=account_key,
                container_name=container_name,
                prefix=prefix
            )

            if success is False:
                logger.error(f"Error occurred while synchronizing Azure Blob.")
                messages.error(request, "An error occurred while synchronizing Azure Blob.")

                return redirect('datasource_media_storages:connect_azure_blob')

        except Exception as e:
            logger.error(f"Error occurred while synchronizing Azure Blob: {str(e)}")
            messages.error(request, "An error occurred while synchronizing Azure Blob.")

            return redirect('datasource_media_storages:connect_azure_blob')

        logger.info(f"Azure Blob synchronization has been completed successfully.")
        messages.success(request, "Azure Blob synchronization has been completed successfully.")

        return redirect('datasource_media_storages:connect_azure_blob')
