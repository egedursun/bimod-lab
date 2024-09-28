from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.llm_core.models import LLMCore
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteLLMCoreView(DeleteView, LoginRequiredMixin):
    """
    Handles the deletion of an LLM Core model.

    This view allows users with the appropriate permissions to delete an LLM Core model and remove it from the associated organization.

    Methods:
        get_context_data(self, **kwargs): Prepares the context with the current user's details.
        post(self, request, *args, **kwargs): Deletes the LLM Core model if the user has the required permissions.
        get_queryset(self): Filters the queryset to include only the LLM Core models associated with the user's organizations.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        context['user'] = user
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - UPDATE_LLM_CORES
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_LLM_CORES):
            messages.error(self.request, "You do not have permission to delete LLM Cores.")
            return redirect('llm_core:list')
        ##############################

        llm_core = get_object_or_404(LLMCore, id=kwargs['pk'])
        llm_core.delete()
        return redirect('llm_core:list')

    def get_queryset(self):
        user = self.request.user
        return LLMCore.objects.filter(organization__in=user.organizations.all())
