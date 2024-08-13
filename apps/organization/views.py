"""
This module contains views for managing organizations within the Bimod.io platform.

The views include creating, listing, updating, deleting organizations, and handling balance-related operations such as adding credits and transferring balances. Access to these views is restricted to authenticated users, with additional permission checks for certain actions.
"""

import decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, DeleteView

from apps.organization.forms import OrganizationForm
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames, UserPermission
from auth.models import PromoCode
from web_project import TemplateLayout


class CreateOrganizationView(TemplateView, LoginRequiredMixin):
    """
    Handles the creation of a new organization within the Bimod.io platform.

    This view displays a form for creating an organization. Upon form submission, it validates the input, checks user permissions, and saves the new organization to the database. If the user lacks the necessary permissions, an error message is displayed.

    Methods:
        get_context_data(self, **kwargs): Adds additional context to the template, including the organization creation form.
        post(self, request, *args, **kwargs): Handles form submission and organization creation, including permission checks and validation.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['form'] = OrganizationForm()
        return context

    def post(self, request, *args, **kwargs):
        form = OrganizationForm(request.POST, request.FILES)
        user = self.request.user
        # PERMISSION CHECK FOR - ORGANIZATION/CREATE
        user_permissions = UserPermission.active_permissions.filter(user=user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.ADD_ORGANIZATIONS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {"Permission Error": "You do not have permission to create organizations."}
            return self.render_to_response(context)

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
    """
    Displays a paginated list of organizations associated with the logged-in user.

    This view retrieves all organizations that the user is part of and displays them in a paginated list.

    Methods:
        get_context_data(self, **kwargs): Retrieves the organizations for the user and adds them to the context with pagination.
    """

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context_user = self.request.user
        organizations = Organization.objects.filter(users__in=[context_user])
        paginator = Paginator(organizations, 10)  # Show 10 organizations per page.
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class OrganizationUpdateView(TemplateView, LoginRequiredMixin):
    """
    Handles updating an existing organization's details.

    This view allows users with the appropriate permissions to modify an organization's attributes. It also handles the form submission and validation for updating the organization.

    Methods:
        get_context_data(self, **kwargs): Retrieves the current organization's details and adds them to the context, along with the organization update form.
        post(self, request, *args, **kwargs): Handles form submission for updating the organization, including permission checks and validation.
    """

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
        # PERMISSION CHECK FOR - ORGANIZATION/UPDATE
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.UPDATE_ORGANIZATIONS not in user_permissions:
            context = self.get_context_data(**kwargs)
            context['error_messages'] = {
                "Permission Error": "You do not have permission to update or modify organizations."}
            return self.render_to_response(context)

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
        organization = self.get_object()
        transfer_organization_id = request.POST.get('transfer_organization_id')
        # Ensure the user has the required permissions
        # PERMISSION CHECK FOR - ORGANIZATION/DELETE
        user_permissions = UserPermission.active_permissions.filter(user=context_user).values_list('permission_type', flat=True)
        if PermissionNames.DELETE_ORGANIZATIONS not in user_permissions:
            messages.error(request, "You do not have permission to delete organizations.")
            return redirect('organization:list')

        # Ensure the transfer organization is valid and belongs to the user
        transfer_organization = get_object_or_404(Organization, id=transfer_organization_id, users__in=[context_user])
        # Transfer the balance to another organization
        transfer_organization.balance += organization.balance
        transfer_organization.save()
        # Delete the organization
        organization.delete()
        print(f"[OrganizationDeleteView.post] Organization {organization.name} has been deleted and the balance has been transferred to {transfer_organization.name}.")
        messages.success(request, f'Organization "{organization.name}" has been deleted and the balance has been transferred to "{transfer_organization.name}".')
        return redirect('organization:list')

    def get_queryset(self):
        context_user = self.request.user
        return Organization.objects.filter(users__in=[context_user])


class OrganizationAddCreditsView(TemplateView, LoginRequiredMixin):
    """
    Handles adding credits to an organization's balance.

    This view allows users to top up their organization's balance. It validates the top-up amount and applies any promo code discounts. If the promo code is valid, the appropriate bonus is added to both the referrer's and referee's organization balances.

    Methods:
        post(self, request, *args, **kwargs): Handles the top-up process, including validation, promo code processing, and updating the organization's balance.
    """

    def post(self, request, *args, **kwargs):
        context_user = self.request.user
        organization_id = kwargs.get('pk')
        organization = get_object_or_404(Organization, id=organization_id, users__in=[context_user])
        topup_amount = request.POST.get('topup_amount')
        promo_code = request.POST.get('promo_code')
        # top up amount can't be zero or negative
        if float(topup_amount) <= 0:
            messages.error(request, 'Top up amount must be greater than zero.')
            return redirect('llm_transaction:list')

        # PERMISSION CHECK FOR - ORGANIZATION/UPDATE
        user_permissions = UserPermission.active_permissions.filter(user=context_user).all().values_list(
            'permission_type', flat=True
        )
        if PermissionNames.UPDATE_ORGANIZATIONS not in user_permissions:
            messages.error(request, "You do not have permission to update or modify organizations.")
            return redirect('llm_transaction:list')

        # try to retrieve the code
        bonus_percentage_referrer, bonus_percentage_referee = 0, 0
        promo_code = PromoCode.objects.filter(code=promo_code).first()
        if promo_code is None:
            bonus_percentage_referee = 0
        else:
            referrer = promo_code.user
            if promo_code.current_referrals + 1 > promo_code.max_referral_limit:
                promo_code.is_active = False
                promo_code.save()
            else:
                promo_code.current_referrals += 1
                bonus_percentage_referrer = promo_code.bonus_percentage_referrer
                bonus_percentage_referee = promo_code.bonus_percentage_referee
                promo_code.save()
                referrer_organization = Organization.objects.filter(users__in=[referrer]).first()
                referrer_organization.balance += decimal.Decimal.from_float(float(float(topup_amount) * ((bonus_percentage_referrer) / 100)))
                referrer_organization.save()
        try:
            topup_amount = float(topup_amount)
            topup_amount += float(float(topup_amount) * (bonus_percentage_referee) / 100)
            organization.balance += decimal.Decimal.from_float(topup_amount)
            organization.save()
            messages.success(request, f'Credits successfully added. New balance: ${organization.balance}')
        except ValueError:
            messages.error(request, 'Invalid amount entered. Please enter a valid number.')
        return redirect('llm_transaction:list')


class OrganizationBalanceTransferView(LoginRequiredMixin, View):
    """
    Handles the transfer of balance between two organizations.

    This view allows users to transfer a specified amount of balance from one of their organizations to another. It ensures that the transfer amount is valid and that the user has sufficient balance in the source organization.

    Methods:
        post(self, request, *args, **kwargs): Handles the balance transfer process, including validation and updating the balances of the source and destination organizations.
    """

    def post(self, request, *args, **kwargs):
        source_org_id = request.POST.get('source_org')
        destination_org_id = request.POST.get('destination_org')
        transfer_amount = request.POST.get('transfer_amount')
        if transfer_amount is None:
            messages.error(request, "Invalid transfer amount.")
            return redirect('llm_transaction:list')
        try:
            transfer_amount = decimal.Decimal(transfer_amount)
        except decimal.InvalidOperation:
            messages.error(request, "Invalid transfer amount.")
            return redirect('llm_transaction:list')
        if transfer_amount <= 0:
            messages.error(request, "Transfer amount must be greater than zero.")
            return redirect('llm_transaction:list')
        if source_org_id == destination_org_id:
            messages.error(request, "Source and destination organizations cannot be the same.")
            return redirect('llm_transaction:list')

        source_org = get_object_or_404(Organization, id=source_org_id, users__in=[request.user])
        destination_org = get_object_or_404(Organization, id=destination_org_id, users__in=[request.user])
        if source_org.balance < transfer_amount:
            messages.error(request, "Insufficient balance in the source organization.")
            return redirect('llm_transaction:list')

        source_org.balance -= transfer_amount
        destination_org.balance += transfer_amount
        source_org.save()
        destination_org.save()
        messages.success(request, f"${transfer_amount} successfully transferred from {source_org.name} to {destination_org.name}.")
        return redirect('llm_transaction:list')


class OrganizationUserAddGiftCreditsView(LoginRequiredMixin, View):
    """
    View to add gift credits from the logged-in user's profile to a specified organization's balance.

    This view handles the transfer of any available free credits from the user's profile to the
    specified organization's balance. If the user has free credits, they are deducted from the
    user's profile and added to the organization's balance. The view handles both success and
    failure cases, providing appropriate feedback to the user via messages.

    Methods:
    --------
    get(request, *args, **kwargs)
        Handles the GET request to perform the gift credits transfer. If successful, the credits
        are added to the organization's balance, and a success message is shown. If there are no
        credits available or an error occurs, an error message is displayed.

    Parameters:
    -----------
    request : HttpRequest
        The HTTP request object.

    args : tuple
        Additional positional arguments.

    kwargs : dict
        Additional keyword arguments, including the organization ID under the key 'pk'.

    Returns:
    --------
    HttpResponseRedirect
        Redirects to the organization list view after attempting the transfer.

    Exceptions:
    -----------
    Raises an exception if there is an error in the process, and an error message is displayed.
    """

    def get(self, request, *args, **kwargs):
        organization_id = kwargs.get('pk')
        user = request.user
        print(f"[OrganizationUserAddGiftCreditsView.get] Adding gift credits to organization {organization_id}.")

        org = get_object_or_404(Organization, id=organization_id, users__in=[request.user])
        user = User.objects.get(id=user.id)
        print(f"[OrganizationUserAddGiftCreditsView.get] Adding gift credits to {org.name}.")
        try:
            if user.profile.free_credits != 0:
                free_credits = user.profile.free_credits
                print(f"[OrganizationUserAddGiftCreditsView.get] Available gift credits: {free_credits} for user '{user.username}'.")
                user.profile.free_credits = 0
                user.profile.save()
                user.save()
                print(f"[OrganizationUserAddGiftCreditsView.get] Updated user profile and user.")
                org.balance += free_credits
                org.save()
                print(f"[OrganizationUserAddGiftCreditsView.get] Updated organization balance.")
                print(f"[OrganizationUserAddGiftCreditsView.get] Gift credits successfully added to {org.name}.")
                messages.success(request, f"Gift credits successfully added to {org.name}.")
            else:
                print(f"[OrganizationUserAddGiftCreditsView.get] No gift credits available to add.")
                messages.error(request, "No gift credits available to add.")
        except Exception as e:
            print(f"[OrganizationUserAddGiftCreditsView.get] Error adding gift credits: {str(e)}")
            messages.error(request, f"Error adding gift credits: {str(e)}")
        return redirect('llm_transaction:list')
