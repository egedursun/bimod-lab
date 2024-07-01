import decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

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
        if form.is_valid():
            organization = form.save(commit=False)
            organization.created_by_user = request.user
            organization.save()
            organization.users.clear()
            organization.users.add(request.user)
            return redirect('organization:list')
        else:
            error_messages = form.errors
            context = self.get_context_data(**kwargs)
            context['form'] = form
            context['error_messages'] = error_messages
            return self.render_to_response(context)


class OrganizationListView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        organizations = Organization.objects.filter(users__in=[context_user])
        context['organizations'] = organizations
        return context


class OrganizationUpdateView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        # retrieve the organization from the ID
        context_user = self.request.user
        organization = Organization.objects.filter(users__in=[context_user], id=kwargs['pk']).first()
        context['organization'] = organization
        context['user'] = context_user
        context['form'] = OrganizationForm(instance=organization)
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user
        organization = get_object_or_404(Organization, users__in=[context_user], id=kwargs['pk'])
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
        context_user = self.request.user
        organization = get_object_or_404(Organization, users__in=[context_user], id=kwargs['pk'])
        organization.delete()
        return redirect('organization:list')

    def get_queryset(self):
        context_user = self.request.user
        return Organization.objects.filter(users__in=[context_user])


class OrganizationAddCreditsView(TemplateView, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):
        context_user = self.request.user
        organization_id = kwargs.get('pk')
        organization = get_object_or_404(Organization, id=organization_id, users__in=[context_user])
        topup_amount = request.POST.get('topup_amount')

        try:
            topup_amount = float(topup_amount)
            organization.balance += decimal.Decimal.from_float(topup_amount)
            organization.save()
            messages.success(request, f'Credits successfully added. New balance: ${organization.balance}')
        except ValueError:
            messages.error(request, 'Invalid amount entered. Please enter a valid number.')

        return redirect('llm_transaction:list')

