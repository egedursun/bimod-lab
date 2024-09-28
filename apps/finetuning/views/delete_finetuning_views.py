from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.finetuning.models import FineTunedModelConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout


class FineTunedModelConnectionRemoveView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['connection'] = get_object_or_404(FineTunedModelConnection, id=kwargs['pk'],
                                                  created_by_user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - DELETE_FINETUNING_MODEL
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_FINETUNING_MODEL):
            messages.error(self.request, "You do not have permission to delete Finetuning Model.")
            return redirect('finetuning:list')
        ##############################

        connection = get_object_or_404(FineTunedModelConnection, id=kwargs['pk'], created_by_user=request.user)
        connection.delete()
        return redirect('finetuning:list')
