from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, UpdateView, DeleteView

from apps.organization.forms import OrganizationForm
from apps.organization.models import Organization
from web_project import TemplateLayout


# Create your views here.

class CreateOrganizationView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = OrganizationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = OrganizationForm(request.POST, request.FILES)
        user = request.user
        form.instance.user = user
        if form.is_valid():
            form.save()
            return redirect('organization:list')
        else:
            error_messsages = form.errors
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['error_messages'] = error_messsages
            return self.render_to_response(context)


class OrganizationListView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user
        organizations = Organization.objects.filter(user=user)
        context['organizations'] = organizations
        return context


class OrganizationUpdateView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        # retrieve the organization from the ID
        user = self.request.user
        organization = Organization.objects.filter(user=user, id=kwargs['pk']).first()
        context['organization'] = organization
        context['user'] = user
        context['form'] = OrganizationForm(instance=organization)
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        organization = get_object_or_404(Organization, user=user, id=kwargs['pk'])
        form = OrganizationForm(request.POST, request.FILES, instance=organization)
        if form.is_valid():
            form.save()
            return redirect('organization:list')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            error_messsages = form.errors
            context['error_messages'] = error_messsages
            return self.render_to_response(context)


class OrganizationDeleteView(DeleteView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        organization = get_object_or_404(Organization, user=user, id=kwargs['pk'])
        organization.delete()
        return redirect('organization:list')

    def get_queryset(self):
        user = self.request.user
        return Organization.objects.filter(user=user)

