from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_codebase.models import CodeRepositoryStorageConnection, CodeBaseRepository, \
    RepositoryProcessingLog
from apps.organization.models import Organization
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListRepositoriesView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_CODE_REPOSITORY
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_CODE_REPOSITORY):
            messages.error(self.request, "You do not have permission to list code repositories.")
            return context
        ##############################

        organizations = Organization.objects.filter(users__in=[request.user])
        data = []
        for org in organizations:
            assistants = Assistant.objects.filter(organization=org)
            assistant_data_list = []
            for assistant in assistants:
                knowledge_bases = CodeRepositoryStorageConnection.objects.filter(assistant=assistant)
                kb_data_list = []
                for kb in knowledge_bases:
                    documents = CodeBaseRepository.objects.filter(knowledge_base=kb).order_by('-created_at')
                    paginator = Paginator(documents, 5)  # 5 repositories per page
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)

                    document_data_list = []
                    for document in page_obj:
                        document: CodeBaseRepository
                        log_entries = RepositoryProcessingLog.objects.filter(
                            repository_full_uri=document.repository_uri)
                        current_statuses = [log.log_message for log in log_entries]
                        document_data_list.append({'document': document, 'current_statuses': current_statuses})
                    kb_data_list.append({
                        'knowledge_base': kb, 'documents': page_obj, 'document_data': document_data_list,
                    })
                assistant_data_list.append({'assistant': assistant, 'knowledge_bases': kb_data_list})
            data.append({'organization': org, 'assistants': assistant_data_list})

        context['data'] = data
        context['document_statuses'] = [
            'staged', 'uploaded', 'loaded', 'chunked', 'embedded_document', 'saved_document', 'processed_document',
            'embedded_chunks', 'saved_chunks', 'processed_chunks', 'completed'
        ]
        context['failed_statuses'] = ['failed']
        context['partially_failed_statuses'] = ['partially_failed']
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        ##############################
        # PERMISSION CHECK FOR - DELETE_CODE_REPOSITORY
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_CODE_REPOSITORY):
            messages.error(self.request, "You do not have permission to add code repositories.")
            return redirect('datasource_codebase:list_repositories')
        ##############################

        document_ids = request.POST.getlist('selected_documents')
        if document_ids:
            CodeBaseRepository.objects.filter(id__in=document_ids).delete()
            messages.success(request, 'Selected repositories deleted successfully.')
            print('[ListRepositoriesView.post] Selected repositories deleted successfully.')
        return redirect('datasource_codebase:list_repositories')
