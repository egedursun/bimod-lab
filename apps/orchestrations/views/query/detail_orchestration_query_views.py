from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.orchestrations.models.query import OrchestrationQuery
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class OrchestrationQueryDetailView(LoginRequiredMixin, TemplateView):
    template_name = "orchestrations/query_detail_orchestration.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - CREATE_AND_USE_ORCHESTRATION_CHATS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CREATE_AND_USE_ORCHESTRATION_CHATS):
            messages.error(self.request, "You do not have permission to create and use orchestration queries.")
            return context
        ##############################

        query_id = self.kwargs.get('query_id')
        query = get_object_or_404(OrchestrationQuery, id=query_id)
        context['query'] = query
        context['logs'] = query.logs.all()
        return context
