from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.leanmod.models import ExpertNetwork
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class ListExpertNetworksView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        ##############################
        # PERMISSION CHECK FOR - LIST_EXPERT_NETWORKS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.LIST_EXPERT_NETWORKS):
            messages.error(self.request, "You do not have permission to list Expert Network.")
            return context
        ##############################

        # Fetch all expert networks and their related assistants
        expert_networks = ExpertNetwork.objects.prefetch_related('assistant_references__assistant',
                                                                 'organization').filter(
            organization__users__in=[self.request.user]
        ).all()

        context['expert_networks'] = expert_networks
        return context
