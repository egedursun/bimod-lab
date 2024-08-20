from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.llm_core.models import LLMCore
from apps.orchestrations.forms import MaestroForm
from apps.orchestrations.models import Maestro
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


class CreateOrchestrationView(LoginRequiredMixin, TemplateView):
    """
    Handles the creation of a new orchestration within the Bimod platform.
    """
    template_name = 'orchestrations/create_orchestration.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = MaestroForm()
        context['organizations'] = Organization.objects.filter(users=self.request.user)
        context['llm_models'] = LLMCore.objects.filter(organization__in=context['organizations'])
        return context

    def post(self, request, *args, **kwargs):
        form = MaestroForm(request.POST, request.FILES)
        user = self.request.user
        # PERMISSION CHECK FOR - ORCHESTRATION/CREATE
        user_permissions = UserPermission.active_permissions.filter(user=user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.ADD_ORCHESTRATIONS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to create orchestrations."}
            return self.render_to_response(context)

        if form.is_valid():
            maestro = form.save(commit=False)
            assistant_image = request.FILES.get('assistant_image')
            maestro.created_by_user = request.user
            maestro.last_updated_by_user = request.user
            maestro.save()
            return redirect('orchestrations:list')
        else:
            error_messages = form.errors
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['error_messages'] = error_messages
            return self.render_to_response(context)


class OrchestrationListView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class OrchestrationQueryView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


class OrchestrationUpdateView(LoginRequiredMixin, TemplateView):
    """
    Handles the update of an existing orchestration within the Bimod.io platform.

    This view displays a form for updating an orchestration. Upon form submission, it validates the input and saves the updated orchestration to the database.
    """

    template_name = 'orchestrations/update_orchestration.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        orchestration = get_object_or_404(Maestro, pk=kwargs['pk'])
        context['form'] = MaestroForm(instance=orchestration)
        context['orchestration'] = orchestration
        context['organizations'] = Organization.objects.filter(users=self.request.user)
        context['llm_models'] = LLMCore.objects.all()  # Pass all LLM models
        return context

    def post(self, request, *args, **kwargs):
        orchestration = get_object_or_404(Maestro, pk=kwargs['pk'])
        form = MaestroForm(request.POST, request.FILES, instance=orchestration)

        if form.is_valid():
            updated_orchestration = form.save(commit=False)
            updated_orchestration.last_updated_by_user = request.user  # Update last_updated_by_user field
            updated_orchestration.save()
            return redirect('orchestrations:list')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['error_messages'] = form.errors
            return self.render_to_response(context)


class OrchestrationDeleteView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
