#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_website_storage_connection_views.py
#  Last Modified: 2024-12-07 19:39:45
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-07 19:39:46
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

from config.settings import (
    MAX_WEBSITE_STORAGES_PER_ASSISTANT
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class DataSourceWebsiteView_StorageCreate(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        user_assistants = Assistant.objects.filter(
            organization__in=user_orgs
        )

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
        # PERMISSION CHECK FOR - ADD_WEBSITE_STORAGES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.ADD_WEBSITE_STORAGES
        ):
            messages.error(self.request, "You do not have permission to add website storage connections.")
            return redirect("datasource_website:storage_list")
        ##############################

        try:

            assistant_id = self.request.POST.get("assistant_id")
            name = self.request.POST.get("name")
            description = self.request.POST.get("description")
            vectorizer = self.request.POST.get("vectorizer")
            embedding_chunk_size = self.request.POST.get("embedding_chunk_size")
            embedding_chunk_overlap = self.request.POST.get("embedding_chunk_overlap")

            if int(embedding_chunk_overlap) >= int(embedding_chunk_size):
                messages.error(self.request, "Embedding chunk overlap must be less than the embedding chunk size.")

                return redirect("datasource_website:storage_create")

            search_instance_retrieval_limit = self.request.POST.get("search_instance_retrieval_limit")
            maximum_pages_to_index = self.request.POST.get("maximum_pages_to_index")

            created_by_user = self.request.user

            assistant = Assistant.objects.get(
                id=assistant_id
            )

            n_website_storages = assistant.datasourcewebsitestorageconnection_set.count()

            if n_website_storages > MAX_WEBSITE_STORAGES_PER_ASSISTANT:
                messages.error(
                    request,
                    f'Assistant has reached the maximum number of website storage connections ({MAX_WEBSITE_STORAGES_PER_ASSISTANT}).'
                )

                return redirect('datasource_website:storage_create')

            if not assistant:
                messages.error(self.request, "Assistant not found.")

                return redirect("datasource_website:storage_create")

            DataSourceWebsiteStorageConnection.objects.create(
                assistant=assistant,
                name=name,
                description=description,
                vectorizer=vectorizer,
                embedding_chunk_size=embedding_chunk_size,
                embedding_chunk_overlap=embedding_chunk_overlap,
                search_instance_retrieval_limit=search_instance_retrieval_limit,
                maximum_pages_to_index=maximum_pages_to_index,
                created_by_user=created_by_user
            )

        except Exception as e:
            logger.error(f"Error while creating website storage connection: {e}")
            messages.error(self.request, "Error while creating website storage connection.")

            return redirect("datasource_website:storage_create")

        messages.success(self.request, "Website storage connection created successfully.")

        return redirect("datasource_website:storage_list")
