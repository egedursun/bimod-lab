from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.finetuning.forms import FineTunedModelConnectionForm
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


class FineTunedModelConnectionAddView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = FineTunedModelConnectionForm()
        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - ADD_FINETUNING_MODEL
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_FINETUNING_MODEL):
            messages.error(self.request, "You do not have permission to add Finetuning Model.")
            return redirect('finetuning:list')
        ##############################

        form = FineTunedModelConnectionForm(request.POST)
        if form.is_valid():
            connection = form.save(commit=False)
            connection.created_by_user = request.user
            connection.save()

        return redirect('finetuning:list')
