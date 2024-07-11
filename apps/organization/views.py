import decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView

from apps.organization.forms import OrganizationForm
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames, UserPermission
from web_project import TemplateLayout


# Create your views here.

class CreateOrganizationView(TemplateView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = OrganizationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = OrganizationForm(request.POST, request.FILES)
        user = self.request.user

        ##############################
        # PERMISSION CHECK FOR - ORGANIZATION/CREATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.ADD_ORGANIZATIONS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to create organizations."}
            return self.render_to_response(context)
        ##############################

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

        ##############################
        # PERMISSION CHECK FOR - ORGANIZATION/LIST
        ##############################
        # For now, we will allow all users to view the list of organizations
        ##############################

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

        ##############################
        # PERMISSION CHECK FOR - ORGANIZATION/UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_ORGANIZATIONS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to update or modify organizations."}
            return self.render_to_response(context)
        ##############################

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
    model = Organization
    context_object_name = 'organization'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_organizations = Organization.objects.filter(users__in=[self.request.user])
        context['user_organizations'] = user_organizations
        context['user_organizations_count'] = user_organizations.count()
        return context

    def post(self, request, *args, **kwargs):
        context_user = self.request.user
        organization = self.get_object()
        transfer_organization_id = request.POST.get('transfer_organization_id')

        # Ensure the user has the required permission
        ##############################
        # PERMISSION CHECK FOR - ORGANIZATION/DELETE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(user=context_user).values_list('permission_type', flat=True)
        if PermissionNames.DELETE_ORGANIZATIONS not in user_permissions:
            messages.error(request, "You do not have permission to delete organizations.")
            return redirect('organization:list')
        ##############################

        # Ensure the transfer organization is valid and belongs to the user
        transfer_organization = get_object_or_404(Organization, id=transfer_organization_id, users__in=[context_user])

        # Transfer the balance to another organization
        transfer_organization.balance += organization.balance
        transfer_organization.save()

        # Delete the organization
        organization.delete()
        messages.success(request, f'Organization "{organization.name}" has been deleted and the balance has been transferred to "{transfer_organization.name}".')
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

        # top up amount can't be zero or negative
        if float(topup_amount) <= 0:
            messages.error(request, 'Top up amount must be greater than zero.')
            return redirect('llm_transaction:list')

        ##############################
        # PERMISSION CHECK FOR - ORGANIZATION/UPDATE
        ##############################
        user_permissions = UserPermission.active_permissions.filter(
            user=context_user
        ).all().values_list(
            'permission_type',
            flat=True
        )
        if PermissionNames.UPDATE_ORGANIZATIONS not in user_permissions:
            messages.error(request, "You do not have permission to update or modify organizations.")
            return redirect('llm_transaction:list')
        ##############################

        try:
            topup_amount = float(topup_amount)
            organization.balance += decimal.Decimal.from_float(topup_amount)
            organization.save()
            messages.success(request, f'Credits successfully added. New balance: ${organization.balance}')
        except ValueError:
            messages.error(request, 'Invalid amount entered. Please enter a valid number.')

        return redirect('llm_transaction:list')

