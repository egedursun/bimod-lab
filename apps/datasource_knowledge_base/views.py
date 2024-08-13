"""
This module contains views for managing document knowledge bases within the Bimod.io platform.

The views include creating, updating, deleting, and listing document knowledge bases and their associated documents. These views also handle uploading documents to the knowledge base and deleting all documents within a specific knowledge base. Access to these views is restricted to authenticated users, with additional permission checks for specific actions.
"""

import boto3
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps._services.knowledge_base.document.knowledge_base_decoder import KnowledgeBaseSystemDecoder
from apps.assistants.models import VECTORIZERS, Assistant
from apps.datasource_knowledge_base.forms import DocumentKnowledgeBaseForm
from apps.datasource_knowledge_base.tasks import index_document_helper, add_document_upload_log
from apps.datasource_knowledge_base.models import KNOWLEDGE_BASE_SYSTEMS, DocumentKnowledgeBaseConnection, \
    KnowledgeBaseDocument, DocumentUploadStatusNames, DocumentProcessingLog
from apps.datasource_knowledge_base.utils import generate_document_uri
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from config import settings
from config.settings import MEDIA_URL
from web_project import TemplateLayout


class DocumentKnowledgeBaseCreateView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of new document knowledge base connections.

    This view displays a form for creating a new knowledge base connection. Upon submission, it validates the input, checks user permissions, and saves the new connection to the database. If the user lacks the necessary permissions, an error message is displayed.

    Methods:
        get_context_data(self, **kwargs): Adds additional context to the template, including available knowledge base systems, vectorizers, and assistants.
        post(self, request, *args, **kwargs): Handles form submission and knowledge base connection creation, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        context['user'] = context_user
        context['knowledge_base_systems'] = KNOWLEDGE_BASE_SYSTEMS
        context['vectorizers'] = VECTORIZERS
        user_organizations = context_user.organizations.all()
        assistants_of_organizations = Assistant.objects.filter(organization__in=user_organizations)
        context['assistants'] = assistants_of_organizations
        context['form'] = DocumentKnowledgeBaseForm()
        return context

    def post(self, request, *args, **kwargs):
        form = DocumentKnowledgeBaseForm(request.POST)
        context_user = self.request.user

        # PERMISSION CHECK FOR - KNOWLEDGE BASE / CREATE
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type',flat=True))
        if PermissionNames.ADD_KNOWLEDGE_BASES not in user_permissions:
            messages.error(request, "You do not have permission to create Knowledge Bases.")
            return redirect('datasource_knowledge_base:list')

        if form.is_valid():
            form.save()
            messages.success(request, "Knowledge Base created successfully.")
            print('[DocumentKnowledgeBaseCreateView.post] Knowledge Base created successfully.')
            return redirect('datasource_knowledge_base:list')
        else:
            messages.error(request, "Error creating Knowledge Base. Please check the form for errors: %s" % form.errors)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class DocumentKnowledgeBaseListView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of document knowledge base connections associated with the user's organizations and assistants.

    This view retrieves all knowledge base connections organized by organization and assistant, and displays them in a structured list.

    Attributes:
        template_name (str): The template used to render the knowledge base list.

    Methods:
        get_context_data(self, **kwargs): Retrieves the knowledge base connections organized by organization and assistant, and adds them to the context.
    """

    template_name = "datasource_knowledge_base/base/list_knowledge_bases.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        user_organizations = Organization.objects.filter(users__in=[context_user])

        connections_by_organization = {}
        for organization in user_organizations:
            assistants = organization.assistants.all()
            assistants_connections = {}
            for assistant in assistants:
                connections = DocumentKnowledgeBaseConnection.objects.filter(assistant=assistant)
                if connections.exists():
                    assistants_connections[assistant] = connections
            if assistants_connections:
                connections_by_organization[organization] = assistants_connections

        context['connections_by_organization'] = connections_by_organization
        context['user'] = context_user
        return context


class DocumentKnowledgeBaseUpdateView(LoginRequiredMixin, TemplateView):
    """
    Handles updating an existing document knowledge base connection.

    This view allows users with the appropriate permissions to modify a knowledge base connection's attributes. It also handles the form submission and validation for updating the connection.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current knowledge base connection details and adds them to the context, along with other relevant data such as available knowledge base systems, vectorizers, and assistants.
        post(self, request, *args, **kwargs): Handles form submission for updating the knowledge base connection, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        knowledge_base = get_object_or_404(DocumentKnowledgeBaseConnection, pk=kwargs['pk'])
        context['user'] = context_user
        context['knowledge_base_systems'] = KNOWLEDGE_BASE_SYSTEMS
        context['vectorizers'] = VECTORIZERS
        user_organizations = context_user.organizations.all()
        assistants_of_organizations = Assistant.objects.filter(organization__in=user_organizations)
        context['assistants'] = assistants_of_organizations
        context['connection'] = knowledge_base
        context['form'] = DocumentKnowledgeBaseForm(instance=knowledge_base)
        return context

    def post(self, request, *args, **kwargs):
        knowledge_base = get_object_or_404(DocumentKnowledgeBaseConnection, pk=kwargs['pk'])
        context_user = self.request.user

        # PERMISSION CHECK FOR - KNOWLEDGE BASE / UPDATE
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_KNOWLEDGE_BASES not in user_permissions:
            messages.error(request, "You do not have permission to update Knowledge Bases.")
            return redirect('datasource_knowledge_base:list')

        form = DocumentKnowledgeBaseForm(request.POST, instance=knowledge_base)
        if form.is_valid():
            form.save()
            messages.success(request, "Knowledge Base updated successfully.")
            print('[DocumentKnowledgeBaseUpdateView.post] Knowledge Base updated successfully.')
            return redirect('datasource_knowledge_base:list')
        else:
            messages.error(request, "Error updating Knowledge Base. Please check the form for errors.")
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class DocumentKnowledgeBaseDeleteView(LoginRequiredMixin, DeleteView):
    """
    Handles the deletion of a document knowledge base connection.

    This view allows users with the appropriate permissions to delete a knowledge base connection. It ensures that the user has the necessary permissions before performing the deletion.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for rendering the confirmation of the deletion.
        post(self, request, *args, **kwargs): Deletes the knowledge base connection if the user has the required permissions.
        get_queryset(self): Filters the queryset to include only the knowledge base connections that belong to the user's assistants.
    """

    model = DocumentKnowledgeBaseConnection
    success_url = '/app/datasource_knowledge_base/list/'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['knowledge_base'] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context_user = self.request.user

        # PERMISSION CHECK FOR - KNOWLEDGE BASE / DELETE
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type',flat=True))
        if PermissionNames.DELETE_KNOWLEDGE_BASES not in user_permissions:
            messages.error(request, "You do not have permission to delete Knowledge Bases.")
            return redirect('datasource_knowledge_base:list')
        print('[DocumentKnowledgeBaseDeleteView.post] Deleting Knowledge Base')
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        context_user = self.request.user
        return DocumentKnowledgeBaseConnection.objects.filter(assistant__organization__users__in=[context_user])


class AddDocumentView(LoginRequiredMixin, TemplateView):
    """
    Handles uploading documents to a selected knowledge base.

    This view displays a form for selecting a knowledge base and uploading documents to it. Upon form submission, it validates the input, uploads the documents to the storage (e.g., S3), and logs the upload process. If the user lacks the necessary permissions, an error message is displayed.

    Methods:
        get(self, request, *args, **kwargs): Prepares the context with the available knowledge bases and assistants for document uploading.
        post(self, request, *args, **kwargs): Handles the document upload process, including validation, file storage, and logging.
    """

    def get(self, request, *args, **kwargs):
        user_assistants = Assistant.objects.filter(organization__users__in=[request.user])
        knowledge_bases = DocumentKnowledgeBaseConnection.objects.filter(assistant__in=user_assistants)
        organizations = Organization.objects.filter(users__in=[request.user])
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = list(organizations.values('id', 'name'))
        context['assistants'] = list(user_assistants.values('id', 'name', 'organization_id'))
        context['knowledge_bases'] = list(knowledge_bases.values('id', 'name', 'assistant_id'))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        knowledge_base_id = request.POST.get('knowledge_base') or None
        context_user = request.user

        # PERMISSION CHECK FOR - DOCUMENT / UPLOAD
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type', flat=True))
        if PermissionNames.ADD_KNOWLEDGE_BASES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to upload documents."}
            return self.render_to_response(context)

        if not knowledge_base_id:
            messages.error(request, 'Please select a knowledge base.')
            return redirect('datasource_knowledge_base:create_documents')
        knowledge_base = DocumentKnowledgeBaseConnection.objects.get(pk=knowledge_base_id)
        files = request.FILES.getlist('document_files')
        if knowledge_base_id and files:
            assistant_base_directory = knowledge_base.assistant.document_base_directory
            file_paths = []
            for file in files:
                file_type = file.name.split('.')[-1]
                document_uri = generate_document_uri(assistant_base_directory, file.name, file_type)
                file_paths.append(document_uri)
                add_document_upload_log(document_full_uri=document_uri, log_name=DocumentUploadStatusNames.STAGED)
                # SAVE the File to s3
                boto3_client = boto3.client('s3')
                bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                s3_path = f"{document_uri.split(MEDIA_URL)[1]}"
                boto3_client.put_object(Bucket=bucket_name, Key=s3_path, Body=file)
                add_document_upload_log(document_full_uri=document_uri, log_name=DocumentUploadStatusNames.UPLOADED)
            # handle the task asynchronously inside the knowledge base system
            KnowledgeBaseSystemDecoder.get(knowledge_base).index_documents(document_paths=file_paths)
            messages.success(request, 'Documents uploaded successfully.')
            print('[AddDocumentView.post] Documents uploaded successfully.')
            return redirect('datasource_knowledge_base:list_documents')
        else:
            messages.error(request, 'Please select a knowledge base and upload documents.')
        return redirect('datasource_knowledge_base:create_documents')


class ListDocumentsView(LoginRequiredMixin, TemplateView):
    """
    Displays a list of documents associated with the user's knowledge bases.

    This view retrieves all documents within the user's knowledge bases, organized by organization and assistant. It also allows users to delete selected documents.

    Methods:
        get(self, request, *args, **kwargs): Retrieves the documents for the user's knowledge bases and adds them to the context, including pagination and status information.
        post(self, request, *args, **kwargs): Handles the deletion of selected documents.
    """

    def get(self, request, *args, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        organizations = Organization.objects.filter(users__in=[request.user])
        data = []
        for org in organizations:
            assistants = Assistant.objects.filter(organization=org)
            assistant_data_list = []
            for assistant in assistants:
                knowledge_bases = DocumentKnowledgeBaseConnection.objects.filter(assistant=assistant)
                kb_data_list = []
                for kb in knowledge_bases:
                    documents = KnowledgeBaseDocument.objects.filter(knowledge_base=kb).order_by('-created_at')
                    paginator = Paginator(documents, 5)  # 5 documents per page
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)

                    document_data_list = []
                    for document in page_obj:
                        log_entries = DocumentProcessingLog.objects.filter(document_full_uri=document.document_uri)
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
        document_ids = request.POST.getlist('selected_documents')
        if document_ids:
            KnowledgeBaseDocument.objects.filter(id__in=document_ids).delete()
            messages.success(request, 'Selected documents deleted successfully.')
            print('[ListDocumentsView.post] Selected documents deleted successfully.')
        return redirect('datasource_knowledge_base:list_documents')


class DeleteAllDocumentsView(LoginRequiredMixin, TemplateView):
    """
    Handles deleting all documents within a specific knowledge base.

    This view allows users with the appropriate permissions to delete all documents in a selected knowledge base. It ensures that the user has the necessary permissions before performing the deletion.

    Methods:
        get_context_data(self, **kwargs): Prepares the context for rendering the confirmation of the deletion.
        post(self, request, *args, **kwargs): Deletes all documents in the selected knowledge base if the user has the required permissions.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        context = self.post(request, *args, **kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        knowledge_base_id = kwargs.get('kb_id')
        context_user = request.user

        # PERMISSION CHECK FOR - DOCUMENT / DELETE
        user_permissions = (UserPermission.active_permissions.filter(user=context_user)
                            .all().values_list('permission_type', flat=True))
        if PermissionNames.DELETE_KNOWLEDGE_BASES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to delete documents."}
            return self.render_to_response(context)

        KnowledgeBaseDocument.objects.filter(knowledge_base_id=knowledge_base_id).delete()
        messages.success(request, 'All documents in the selected knowledge base have been deleted successfully.')
        print('[DeleteAllDocumentsView.post] All documents in the selected knowledge base have been deleted successfully.')
        return redirect('datasource_knowledge_base:list_documents')
