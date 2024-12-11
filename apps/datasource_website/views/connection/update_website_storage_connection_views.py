#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_website_storage_connections_views.py
#  Last Modified: 2024-12-07 19:40:02
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 19:40:03
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

from django.views.generic import (
    TemplateView
)

from apps.assistants.models import Assistant

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.datasource_knowledge_base.utils import (
    EMBEDDING_VECTORIZER_MODELS
)

from apps.datasource_website.models import (
    DataSourceWebsiteStorageConnection
)

from apps.organization.models import Organization

from apps.user_permissions.utils import (
    PermissionNames
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class DataSourceWebsiteView_StorageUpdate(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        storage_item = DataSourceWebsiteStorageConnection.objects.get(
            id=self.kwargs.get("pk")
        )

        if not storage_item:
            logger.error(f"Error while updating website storage connection: Website storage connection not found.")
            messages.error(self.request, "Website storage connection not found.")

            return redirect("datasource_website:storage_list")

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        user_assistants = Assistant.objects.filter(
            organization__in=user_orgs
        )

        context["connection"] = storage_item
        context["assistants"] = user_assistants
        context["vectorizers"] = EMBEDDING_VECTORIZER_MODELS

        return context

    def post(
        self,
        request,
        *args,
        **kwargs
    ):
        ##############################
        # PERMISSION CHECK FOR - UPDATE_WEBSITE_STORAGES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_WEBSITE_STORAGES
        ):
            messages.error(self.request, "You do not have permission to update website storage connections.")
            return redirect("datasource_website:storage_list")
        ##############################

        try:

            assistant_id = self.request.POST.get("assistant_id")
            name = self.request.POST.get("name")
            description = self.request.POST.get("description")

            vectorizer = self.request.POST.get("vectorizer")
            embedding_chunk_size = self.request.POST.get("embedding_chunk_size")
            embedding_chunk_overlap = self.request.POST.get("embedding_chunk_overlap")

            search_instance_retrieval_limit = self.request.POST.get("search_instance_retrieval_limit")
            maximum_pages_to_index = self.request.POST.get("maximum_pages_to_index")
            created_by_user = self.request.user

            assistant = Assistant.objects.get(
                id=assistant_id
            )

            if not assistant:
                messages.error(self.request, "Assistant not found.")

                return redirect("datasource_website:storage_update")

            item = DataSourceWebsiteStorageConnection.objects.get(
                id=self.kwargs.get("pk")
            )

            if not item:
                logger.error(f"Error while updating website storage connection: Website storage connection not found.")
                messages.error(self.request, "Website storage connection not found.")

                return redirect("datasource_website:storage_update")

            item.assistant = assistant
            item.name = name
            item.description = description

            item.vectorizer = vectorizer
            item.embedding_chunk_size = embedding_chunk_size
            item.embedding_chunk_overlap = embedding_chunk_overlap

            item.search_instance_retrieval_limit = search_instance_retrieval_limit
            item.maximum_pages_to_index = maximum_pages_to_index
            item.created_by_user = created_by_user

            item.save()

        except Exception as e:
            logger.error(f"Error while updating website storage connection: {e}")
            messages.error(self.request, "Error while updating website storage connection.")

            return redirect("datasource_website:storage_update")

        messages.success(self.request, "Website storage connection updated successfully.")

        return redirect("datasource_website:storage_list")
