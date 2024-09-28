from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.orchestrations.models.query import OrchestrationQuery
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class OrchestrationQueryDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'orchestrations/query_confirm_delete_orchestration.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        query_id = self.kwargs['query_id']
        context['query'] = get_object_or_404(OrchestrationQuery, pk=query_id)
        context['orchestration'] = context['query'].maestro
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - REMOVE_ORCHESTRATION_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.REMOVE_ORCHESTRATION_CHATS):
            messages.error(self.request, "You do not have permission to remove orchestration queries.")
            return redirect('orchestrations:list')
        ##############################

        query_id = self.kwargs['query_id']
        query = get_object_or_404(OrchestrationQuery, pk=query_id)
        maestro_id = query.maestro.id
        query.delete()
        return redirect('orchestrations:query_list', pk=maestro_id)
