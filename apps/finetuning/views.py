from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.finetuning.forms import FineTunedModelConnectionForm
from apps.finetuning.models import FineTunedModelConnection, FineTuningModelProvidersNames, FineTunedModelTypesNames
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


class FineTunedModelConnectionAddView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = FineTunedModelConnectionForm()
        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user

        # PERMISSION CHECK FOR - LLM CORES
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.ADD_LLM_CORES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add LLM Models."}
            return self.render_to_response(context)

        form = FineTunedModelConnectionForm(request.POST)
        if form.is_valid():
            connection = form.save(commit=False)
            connection.created_by_user = request.user
            connection.save()

        return redirect('finetuning:list')


class FineTunedModelConnectionRemoveView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['connection'] = get_object_or_404(FineTunedModelConnection, id=kwargs['pk'], created_by_user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user

        # PERMISSION CHECK FOR - LLM CORES
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.DELETE_LLM_CORES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to delete LLM Models."}
            return self.render_to_response(context)

        connection = get_object_or_404(FineTunedModelConnection, id=kwargs['pk'], created_by_user=request.user)
        connection.delete()
        return redirect('finetuning:list')


class FineTunedModelConnectionsListView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Fetch organizations associated with the user
        organizations = Organization.objects.filter(users__in=[self.request.user])
        data = []

        for organization in organizations:
            # Fetch fine-tuned model connections for each organization
            connections = FineTunedModelConnection.objects.filter(
                organization=organization,
                created_by_user=self.request.user
            )
            data.append({'organization': organization, 'connections': connections})

        context['data'] = data
        # Add form-related context
        context['form'] = FineTunedModelConnectionForm()
        context['organizations'] = organizations
        context['providers'] = FineTuningModelProvidersNames.as_list()
        context['model_types'] = FineTunedModelTypesNames.as_list()
        return context

    def post(self, request, *args, **kwargs):
        form = FineTunedModelConnectionForm(request.POST)
        if form.is_valid():
            connection = form.save(commit=False)
            connection.created_by_user = request.user
            connection.save()
            return redirect('finetuning:list')

        # Re-render the page with form errors
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
