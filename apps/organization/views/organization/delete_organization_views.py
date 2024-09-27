from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DeleteView

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.llm_transaction.models import TransactionInvoice, InvoiceTypesNames, PaymentMethodsNames
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames
from web_project import TemplateLayout


class OrganizationDeleteView(DeleteView, LoginRequiredMixin):
    """
    Handles the deletion of an organization.

    This view allows users with the appropriate permissions to delete an organization. It ensures that the user has the necessary permissions and transfers the organization's balance to another specified organization before deletion.

    Methods:
        get_context_data(self, **kwargs): Adds the organization to be deleted to the context, along with the user's organizations for balance transfer.
        post(self, request, *args, **kwargs): Deletes the organization if the user has the required permissions and transfers the balance to another organization.
        get_queryset(self): Filters the queryset to include only the organizations that belong to the user's organizations.
    """

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

        ##############################
        # PERMISSION CHECK FOR - DELETE_ORGANIZATIONS
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.DELETE_ORGANIZATIONS):
            messages.error(self.request, "You do not have permission to delete organizations.")
            return redirect('organization:list')
        ##############################

        organization = self.get_object()
        transfer_organization_id = request.POST.get('transfer_organization_id')

        # Ensure the transfer organization is valid and belongs to the user
        transfer_organization = get_object_or_404(Organization, id=transfer_organization_id, users__in=[context_user])
        # Transfer the balance to another organization
        source_organization_balance = organization.balance
        transfer_organization.balance += organization.balance
        transfer_organization.save()

        ############################################
        # Create the invoice for the transaction
        TransactionInvoice.objects.create(
            organization=organization,
            responsible_user=context_user,
            transaction_type=InvoiceTypesNames.TRANSFERRED_CREDITS,
            amount_added=source_organization_balance,
            payment_method=PaymentMethodsNames.INTERNAL_TRANSFER,
        )
        ############################################

        # Delete the organization
        organization.delete()
        print(
            f"[OrganizationDeleteView.post] Organization {organization.name} has been deleted and the balance has been transferred to {transfer_organization.name}.")
        messages.success(request,
                         f'Organization "{organization.name}" has been deleted and the balance has been transferred to "{transfer_organization.name}".')
        return redirect('organization:list')

    def get_queryset(self):
        context_user = self.request.user
        return Organization.objects.filter(users__in=[context_user])
