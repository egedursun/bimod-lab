import time

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps.llm_core.forms import LLMCoreForm
from apps.llm_core.models import LLM_CORE_PROVIDERS, OPENAI_GPT_MODEL_NAMES, LLMCore
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames, UserPermission
from web_project import TemplateLayout


# Create your views here.

class CreateLLMCoreView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        context['user'] = user
        context['organizations'] = user.organizations.all()
        context['provider_choices'] = LLM_CORE_PROVIDERS
        context['model_name_choices'] = OPENAI_GPT_MODEL_NAMES
        return context

    def post(self, request, *args, **kwargs):
        form = LLMCoreForm(request.POST, request.FILES)
        user = request.user

        ##############################
        # PERMISSION CHECK FOR - LLM/CREATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_LLM_CORES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to add LLM Cores."}
            return self.render_to_response(context)
        ##############################

        form.instance.created_by_user = user
        form.instance.last_updated_by_user = user
        if form.is_valid():
            form.save()
            # add llm model to the organization
            organization = Organization.objects.get(id=request.POST['organization'])
            llm_core = LLMCore.objects.filter(created_by_user=user).latest('created_at')
            organization.llm_cores.add(llm_core)
            organization.save()
            return redirect('llm_core:list')
        else:
            error_messages = form.errors
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['error_messages'] = error_messages
            return self.render_to_response(context)


class ListLLMCoreView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        organizations = user.organizations.all()

        ##############################
        # PERMISSION CHECK FOR - LLM/LIST
        ##############################
        # For now, every user is able to see the LLM cores.
        ##############################

        # retrieve the llm cores for every organization and store in the dictionary
        llm_cores = {}
        for organization in organizations:
            llm_cores[organization] = organization.llm_cores.all()
        context['organizations'] = organizations
        context['org_llm_cores'] = llm_cores
        return context


class UpdateLLMCoreView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        llm_core = LLMCore.objects.get(id=kwargs['pk'])
        context_user = self.request.user
        context['llm_core'] = llm_core
        context['organizations'] = context_user.organizations.all()
        context['provider_choices'] = LLM_CORE_PROVIDERS
        context['model_name_choices'] = OPENAI_GPT_MODEL_NAMES
        return context

    def post(self, request, *args, **kwargs):
        llm_core = LLMCore.objects.get(id=kwargs['pk'])
        prev_organization = llm_core.organization
        print("LLM Core of Operation: ", llm_core)
        form = LLMCoreForm(request.POST, request.FILES, instance=llm_core)
        print("Form.OrganizationData: ", request.POST['organization'])
        context_user = request.user
        print("User of Operation: ", context_user)

        ##############################
        # PERMISSION CHECK FOR - LLM/UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_LLM_CORES not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to update or modify LLM Cores."}
            return self.render_to_response(context)
        ##############################

        if form.is_valid():
            prev_organization.llm_cores.remove(llm_core)
            prev_organization.save()
            form.save()
            organization = Organization.objects.get(id=request.POST['organization'])
            organization.llm_cores.add(llm_core)
            organization.save()
            return redirect('llm_core:list')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            error_messages = form.errors
            context['error_messages'] = error_messages
            return self.render_to_response(context)


class DeleteLLMCoreView(DeleteView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        context['user'] = user
        return context

    def post(self, request, *args, **kwargs):
        user = request.user

        ##############################
        # PERMISSION CHECK FOR - LLM/DELETE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.DELETE_LLM_CORES not in user_permissions:
            messages.error(request, "You do not have permission to delete LLM Cores.")
            return redirect('llm_core:list')
        ##############################

        llm_core = get_object_or_404(LLMCore, id=kwargs['pk'])
        llm_core.delete()
        return redirect('llm_core:list')

    def get_queryset(self):
        user = self.request.user
        return LLMCore.objects.filter(organizations__in=user.organizations.all())
