from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps.llm_core.forms import LLMCoreForm
from apps.llm_core.models import LLM_CORE_PROVIDERS, OPENAI_GPT_MODEL_NAMES, LLMCore
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
        form.instance.created_by_user = user
        form.instance.last_updated_by_user = user
        if form.is_valid():
            form.save()
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
        org_llm_cores = {}
        for organization in organizations:
            llm_cores = LLMCore.objects.filter(organization=organization)
            org_llm_cores[organization] = llm_cores
        context['org_llm_cores'] = org_llm_cores
        return context


class UpdateLLMCoreView(TemplateView, LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        llm_core = LLMCore.objects.get(id=kwargs['pk'])
        context['llm_core'] = llm_core
        context['organizations'] = llm_core.organization.user.organizations.all()
        context['provider_choices'] = LLM_CORE_PROVIDERS
        context['model_name_choices'] = OPENAI_GPT_MODEL_NAMES
        return context

    def post(self, request, *args, **kwargs):
        llm_core = LLMCore.objects.get(id=kwargs['pk'])
        form = LLMCoreForm(request.POST, request.FILES, instance=llm_core)
        if form.is_valid():
            form.save()
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
        llm_core = get_object_or_404(LLMCore, id=kwargs['pk'])
        llm_core.delete()
        return redirect('llm_core:list')

    def get_queryset(self):
        user = self.request.user
        return LLMCore.objects.filter(organization__in=user.organizations.all())
