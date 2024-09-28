from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.leanmod.models import ExpertNetwork
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class DeleteExpertNetworkView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        expert_network_id = kwargs.get('pk')
        expert_network = get_object_or_404(ExpertNetwork, id=expert_network_id)
        context['expert_network'] = expert_network
        return context

    def post(self, request, *args, **kwargs):
        ##############################
        # PERMISSION CHECK FOR - DELETE_EXPERT_NETWORKS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_EXPERT_NETWORKS):
            messages.error(self.request, "You do not have permission to delete Expert Network.")
            return redirect('leanmod:list_expert_networks')
        ##############################

        expert_network_id = kwargs.get('pk')
        expert_network = get_object_or_404(ExpertNetwork, id=expert_network_id)

        # Perform the deletion
        expert_network.delete()

        messages.success(request, f'The expert network "{expert_network.name}" has been deleted successfully.')
        return redirect('leanmod:list_expert_networks')
