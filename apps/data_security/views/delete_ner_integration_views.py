from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.data_security.models import NERIntegration
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteNERIntegrationView(LoginRequiredMixin, TemplateView):
    template_name = 'data_security/ner/confirm_delete_ner_integration.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        ner_integration = get_object_or_404(NERIntegration, id=self.kwargs['pk'])
        context['ner_integration'] = ner_integration
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_DATA_SECURITY
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_DATA_SECURITY):
            messages.error(self.request, "You do not have permission to delete data security layers.")
            return redirect('data_security:list_ner_integrations')
        ##############################

        ner_integration = get_object_or_404(NERIntegration, id=self.kwargs['pk'])
        # If you want, you can add more logic here (e.g., checking permissions)
        ner_integration.delete()
        messages.success(request, 'NER Policy has been deleted successfully.')
        return redirect('data_security:list_ner_integrations')
