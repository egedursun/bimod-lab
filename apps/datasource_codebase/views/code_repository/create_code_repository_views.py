#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: create_code_repository_views.py
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
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.codebase.codebase_decoder import CodeBaseDecoder
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_codebase.models import CodeRepositoryStorageConnection
from apps.datasource_codebase.tasks import add_repository_upload_log
from apps.datasource_codebase.utils import RepositoryUploadStatusNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class CodeBaseView_RepositoryCreate(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user_agents = Assistant.objects.filter(organization__users__in=[request.user])
        vector_stores = CodeRepositoryStorageConnection.objects.filter(assistant__in=user_agents)
        orgs = Organization.objects.filter(users__in=[request.user])
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = list(orgs.values('id', 'name'))
        context['assistants'] = list(user_agents.values('id', 'name', 'organization_id'))
        context['knowledge_bases'] = list(vector_stores.values('id', 'name', 'assistant_id'))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        vs_id = request.POST.get('knowledge_base') or None

        ##############################
        # PERMISSION CHECK FOR - ADD_CODE_REPOSITORY
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_CODE_REPOSITORY):
            messages.error(self.request, "You do not have permission to add code repositories.")
            return redirect('datasource_codebase:list_repositories')
        ##############################

        if not vs_id:
            messages.error(request, 'Please select a knowledge base.')
            return redirect('datasource_knowledge_base:create_documents')
        vector_store = CodeRepositoryStorageConnection.objects.get(pk=vs_id)
        repo_url = request.POST.get('repository_url')
        if vs_id and repo_url:
            add_repository_upload_log(document_full_uri=repo_url, log_name=RepositoryUploadStatusNames.STAGED)
            add_repository_upload_log(document_full_uri=repo_url, log_name=RepositoryUploadStatusNames.UPLOADED)
            CodeBaseDecoder.get(vector_store).index_repositories(document_paths=[repo_url])
            messages.success(request, 'Repositories uploaded successfully.')
            return redirect('datasource_codebase:list_repositories')
        else:
            messages.error(request, 'Please select a knowledge base and add repositories.')
        return redirect('datasource_codebase:create_repositories')
