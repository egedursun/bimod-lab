from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps.assistants.models import Assistant
from apps.memories.models import AssistantMemory
from apps.organization.models import Organization
from apps.user_permissions.models import UserPermission, PermissionNames
from web_project import TemplateLayout


MEMORY_TYPE = [
    ("user-specific", "User-Specific"),
    ("assistant-specific", "Assistant-Specific"),
]


class MemoryTypeNames:
    USER_SPECIFIC = "user-specific"
    ASSISTANT_SPECIFIC = "assistant-specific"


class ListAssistantMemoryView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        org_assistants = {}
        organizations = Organization.objects.filter(users=self.request.user)
        for organization in organizations:
            assistants = Assistant.objects.filter(organization=organization)
            org_assistants[organization] = []
            for assistant in assistants:
                assistant_specific_memories = AssistantMemory.objects.filter(
                    assistant=assistant,
                    memory_type=MemoryTypeNames.ASSISTANT_SPECIFIC
                )
                user_specific_memories = AssistantMemory.objects.filter(
                    assistant=assistant,
                    memory_type=MemoryTypeNames.USER_SPECIFIC,
                    user=self.request.user
                )
                memories = list(assistant_specific_memories) + list(user_specific_memories)
                org_assistants[organization].extend(memories)

        context['org_assistants'] = org_assistants
        return context


class CreateAssistantMemoryView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        assistants = Assistant.objects.filter(organization__users=user)
        context.update({'assistants': assistants})
        return context

    def post(self, request, *args, **kwargs):
        assistant_id = request.POST.get('assistant')
        memory_type = request.POST.get('memory_type')
        memory_text_content = request.POST.get('memory_text_content')
        context_user = request.user
        # PERMISSION CHECK FOR - MEMORIES CREATION
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.ADD_ASSISTANT_MEMORIES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to create memories."}
            return self.render_to_response(context)

        AssistantMemory.objects.create(
            user=request.user, assistant_id=assistant_id, memory_type=memory_type,
            memory_text_content=memory_text_content
        )
        # add the memory to the assistant memories
        # Note: the specificity of the memory is handled in prompt management module
        assistant = Assistant.objects.get(id=assistant_id)
        assistant.memories.add(AssistantMemory.objects.last())
        return redirect('memories:list')


class DeleteAssistantMemoryView(LoginRequiredMixin, DeleteView):
    model = AssistantMemory
    success_url = 'memories:list'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context_user = request.user
        memory = get_object_or_404(AssistantMemory, id=self.kwargs['pk'])
        # PERMISSION CHECK FOR - MEMORIES DELETION
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.DELETE_ASSISTANT_MEMORIES not in user_permissions:
            messages.error(request, "You do not have permission to delete memories.")
            return redirect('memories:list')

        memory.delete()
        success_message = "Memory deleted successfully!"
        messages.success(request, success_message)
        return redirect(self.success_url)
