from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.datasource_knowledge_base.models import KnowledgeBaseDocument
from apps.user_permissions.models import PermissionNames


class DeleteAllKnowledgeBaseDocumentsView(View, LoginRequiredMixin):
    """
    Handles the deletion of all knowledge base documents associated with the user account.
    """

    def post(self, request, *args, **kwargs):
        user = request.user
        user_knowledge_base_documents = KnowledgeBaseDocument.objects.filter(
            knowledge_base__assistant__organization__users__in=[user]
        ).all()
        confirmation_field = request.POST.get('confirmation', None)

        # [1] Validate deletion request
        if confirmation_field != 'CONFIRM DELETING ALL KNOWLEDGE BASE DOCUMENTS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL KNOWLEDGE BASE DOCUMENTS'.")
            return redirect('user_settings:settings')

        # [2] Verify permissions for the bulk deletion operation
        ##############################
        # PERMISSION CHECK FOR - DELETE_KNOWLEDGE_BASE_DOCS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_KNOWLEDGE_BASE_DOCS):
            messages.error(self.request, "You do not have permission to delete knowledge base documents.")
            return redirect('user_settings:settings')
        ##############################

        # [3] Delete ALL items in the queryset
        try:
            for knowledge_base_document in user_knowledge_base_documents:
                knowledge_base_document.delete()
            messages.success(request, "All knowledge base documents associated with your account have been deleted.")
        except Exception as e:
            messages.error(request, f"Error deleting knowledge base documents: {e}")

        # [4] Redirect back to settings page
        return redirect('user_settings:settings')
