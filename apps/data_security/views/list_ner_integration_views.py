from django.contrib import messages
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.data_security.models import NERIntegration
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


class ListNERIntegrationsView(TemplateView):
    template_name = 'data_security/ner/list_ner_integrations.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - ADD_DATA_SECURITY
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_DATA_SECURITY):
            messages.error(self.request, "You do not have permission to list data security layers.")
            return context
        ##############################

        context['ner_integrations'] = NERIntegration.objects.select_related('organization').all()
        return context
