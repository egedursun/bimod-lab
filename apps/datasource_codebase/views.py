from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps._services.codebase.codebase_decoder import CodeBaseDecoder
from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.assistants.models import Assistant
from apps.datasource_codebase.forms import CodeRepositoryStorageForm
from apps.datasource_codebase.models import KNOWLEDGE_BASE_SYSTEMS, VECTORIZERS, CodeRepositoryStorageConnection, \
    RepositoryUploadStatusNames, CodeBaseRepository, RepositoryProcessingLog
from apps.datasource_codebase.tasks import add_repository_upload_log
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


class CodeBaseStorageCreateView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        context['user'] = context_user
        context['knowledge_base_systems'] = KNOWLEDGE_BASE_SYSTEMS
        context['vectorizers'] = VECTORIZERS
        user_organizations = context_user.organizations.all()
        assistants_of_organizations = Assistant.objects.filter(organization__in=user_organizations)
        context['assistants'] = assistants_of_organizations
        context['form'] = CodeRepositoryStorageForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CodeRepositoryStorageForm(request.POST)
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_CODE_BASE
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_CODE_BASE):
            messages.error(self.request, "You do not have permission to add code base storages.")
            return redirect('datasource_codebase:list')
        ##############################

        if form.is_valid():
            form.save()
            messages.success(request, "Code Base Storage created successfully.")
            print('[CodeBaseStorageCreateView.post] Code Base Storage created successfully.')
            return redirect('datasource_codebase:list')
        else:
            messages.error(request, "Error creating Code Base Storage. Please check the form for errors.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class CodeBaseStorageListView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_CODE_BASE
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_CODE_BASE):
            messages.error(self.request, "You do not have permission to list code base storages.")
            return context
        ##############################

        context_user = self.request.user
        user_organizations = Organization.objects.filter(users__in=[context_user])

        connections_by_organization = {}
        for organization in user_organizations:
            assistants = organization.assistants.all()
            assistants_connections = {}
            for assistant in assistants:
                connections = CodeRepositoryStorageConnection.objects.filter(assistant=assistant)
                if connections.exists():
                    assistants_connections[assistant] = connections
            if assistants_connections:
                connections_by_organization[organization] = assistants_connections

        context['connections_by_organization'] = connections_by_organization
        context['user'] = context_user
        return context


class CodeBaseStorageUpdateView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        knowledge_base = get_object_or_404(CodeRepositoryStorageConnection, pk=kwargs['pk'])
        context['user'] = context_user
        context['knowledge_base_systems'] = KNOWLEDGE_BASE_SYSTEMS
        context['vectorizers'] = VECTORIZERS
        user_organizations = context_user.organizations.all()
        assistants_of_organizations = Assistant.objects.filter(organization__in=user_organizations)
        context['assistants'] = assistants_of_organizations
        context['connection'] = knowledge_base
        context['form'] = CodeRepositoryStorageForm(instance=knowledge_base)
        return context

    def post(self, request, *args, **kwargs):
        knowledge_base = get_object_or_404(CodeRepositoryStorageConnection, pk=kwargs['pk'])
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - UPDATE_CODE_BASE
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.UPDATE_CODE_BASE):
            messages.error(self.request, "You do not have permission to update code base storages.")
            return redirect('datasource_codebase:list')
        ##############################

        form = CodeRepositoryStorageForm(request.POST, instance=knowledge_base)
        if form.is_valid():
            form.save()
            messages.success(request, "Code Base Storage updated successfully.")
            print('[CodeBaseStorageUpdateView.post] Code Base Storage updated successfully.')
            return redirect('datasource_codebase:list')
        else:
            messages.error(request, "Error updating Code Base Storage. Please check the form for errors.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class CodeBaseStorageDeleteView(LoginRequiredMixin, DeleteView):
    model = CodeRepositoryStorageConnection
    success_url = '/app/datasource_codebase/list/'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['knowledge_base'] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - DELETE_CODE_BASE
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_CODE_BASE):
            messages.error(self.request, "You do not have permission to update code base storages.")
            return redirect('datasource_codebase:list')
        ##############################

        print('[CodeBaseStorageDeleteView.post] Code Base Storage deleted successfully.')
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        context_user = self.request.user
        return CodeRepositoryStorageConnection.objects.filter(assistant__organization__users__in=[context_user])


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


class DeleteAllRepositoriesView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.post(request, *args, **kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        knowledge_base_id = kwargs.get('kb_id')
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - DELETE_CODE_REPOSITORY
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_CODE_REPOSITORY):
            messages.error(self.request, "You do not have permission to delete code repositories.")
            return redirect('datasource_codebase:list_repositories')
        ##############################

        CodeBaseRepository.objects.filter(knowledge_base_id=knowledge_base_id).delete()
        messages.success(request, 'All repositories in the selected knowledge base have been deleted successfully.')
        print(
            '[DeleteAllRepositoriesView.post] All repositories in the selected knowledge base have been deleted successfully.')
        return redirect('datasource_codebase:list_repositories')
