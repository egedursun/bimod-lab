from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps.assistants.models import Assistant
from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


# Create your views here.

class CreateAssistantView(LoginRequiredMixin, TemplateView):
    template_name = "assistants/create_assistant.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        context['llm_models'] = LLMCore.objects.filter(organization__in=context['organizations'])
        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - ASSISTANT/CREATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_ASSISTANTS not in user_permissions:
            messages.error(request, "You do not have permission to create assistants.")
            return redirect('assistants:list')
        ##############################

        organization_id = request.POST.get('organization')
        llm_model_id = request.POST.get('llm_model')
        name = request.POST.get('name')
        description = request.POST.get('description')
        instructions = request.POST.get('instructions')
        response_template = request.POST.get('response_template')
        audience = request.POST.get('audience')
        tone = request.POST.get('tone')
        assistant_image = request.FILES.get('assistant_image')

        if not (organization_id and llm_model_id and name and description and instructions and audience and tone):
            messages.error(request, "All fields are required.")
            return redirect('assistants:create')

        organization = Organization.objects.get(id=organization_id)
        llm_model = LLMCore.objects.get(id=llm_model_id)

        assistant = Assistant.objects.create(
            organization=organization,
            llm_model=llm_model,
            name=name,
            description=description,
            instructions=instructions,
            audience=audience,
            tone=tone,
            assistant_image=assistant_image,
            created_by_user=context_user,
            last_updated_by_user=context_user,
            response_templates=response_template
        )

        # retrieve the assistants of the organization and add the new assistant
        organization.organization_assistants.add(assistant)
        organization.save()

        messages.success(request, "Assistant created successfully!")
        return redirect('assistants:list')


class ListAssistantView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ASSISTANT/CREATE
        ##############################
        # for now, we will allow all users to view the list of assistants...
        ##############################

        organizations = Organization.objects.filter(users__in=[user])
        org_assistants = {org: org.assistants.all() for org in organizations}
        context['org_assistants'] = org_assistants
        return context


class UpdateAssistantView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        assistant_id = self.kwargs.get('pk')
        assistant = get_object_or_404(Assistant, id=assistant_id)
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        context['llm_models'] = LLMCore.objects.filter(organization__in=context['organizations'])
        context['assistant'] = assistant
        return context

    def post(self, request, *args, **kwargs):
        context_user = request.user

        ##############################
        # PERMISSION CHECK FOR - ASSISTANT/UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_ASSISTANTS not in user_permissions:
            messages.error(request, "You do not have permission to update / modify assistants.")
            return redirect('assistants:list')
        ##############################

        assistant_id = self.kwargs.get('pk')
        assistant = get_object_or_404(Assistant, id=assistant_id)
        assistant.name = request.POST.get('name')
        assistant.description = request.POST.get('description')
        assistant.instructions = request.POST.get('instructions')
        assistant.audience = request.POST.get('audience')
        assistant.tone = request.POST.get('tone')
        assistant.llm_model_id = request.POST.get('llm_model')
        assistant.response_template = request.POST.get('response_template')
        assistant.last_updated_by_user = request.user
        if 'assistant_image' in request.FILES:
            assistant.assistant_image = request.FILES['assistant_image']
        assistant.save()

        return redirect('assistants:update', pk=assistant.id)


class DeleteAssistantView(LoginRequiredMixin, DeleteView):
    model = Assistant

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        assistant = self.get_object()
        context['assistant'] = assistant
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ASSISTANT/CREATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_ASSISTANTS not in user_permissions:
            messages.error(request, "You do not have permission to delete assistants.")
            return redirect('assistants:list')
        ##############################

        assistant = self.get_object()
        assistant.delete()
        return redirect('assistants:list')

    def get_queryset(self):
        context_user = self.request.user
        return Assistant.objects.filter(organization__users__in=[context_user])
