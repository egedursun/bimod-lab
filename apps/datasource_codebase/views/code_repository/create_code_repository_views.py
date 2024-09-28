from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.codebase.codebase_decoder import CodeBaseDecoder
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_codebase.models import CodeRepositoryStorageConnection
from apps.datasource_codebase.tasks import add_repository_upload_log
from apps.datasource_codebase.utils import RepositoryUploadStatusNames
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class AddRepositoryView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user_assistants = Assistant.objects.filter(organization__users__in=[request.user])
        knowledge_bases = CodeRepositoryStorageConnection.objects.filter(assistant__in=user_assistants)
        organizations = Organization.objects.filter(users__in=[request.user])
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = list(organizations.values('id', 'name'))
        context['assistants'] = list(user_assistants.values('id', 'name', 'organization_id'))
        context['knowledge_bases'] = list(knowledge_bases.values('id', 'name', 'assistant_id'))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        knowledge_base_id = request.POST.get('knowledge_base') or None
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_CODE_REPOSITORY
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_CODE_REPOSITORY):
            messages.error(self.request, "You do not have permission to add code repositories.")
            return redirect('datasource_codebase:list_repositories')
        ##############################

        if not knowledge_base_id:
            messages.error(request, 'Please select a knowledge base.')
            return redirect('datasource_knowledge_base:create_documents')
        knowledge_base = CodeRepositoryStorageConnection.objects.get(pk=knowledge_base_id)
        repository_url = request.POST.get('repository_url')
        if knowledge_base_id and repository_url:
            add_repository_upload_log(document_full_uri=repository_url, log_name=RepositoryUploadStatusNames.STAGED)
            add_repository_upload_log(document_full_uri=repository_url, log_name=RepositoryUploadStatusNames.UPLOADED)
            # handle the task asynchronously inside the knowledge base system
            CodeBaseDecoder.get(knowledge_base).index_repositories(document_paths=[repository_url])
            messages.success(request, 'Repositories uploaded successfully.')
            print('[AddRepositoryView.post] Repositories uploaded successfully.')
            return redirect('datasource_codebase:list_repositories')
        else:
            messages.error(request, 'Please select a knowledge base and add repositories.')
        return redirect('datasource_codebase:create_repositories')
