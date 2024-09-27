import decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.views import View

from apps._services.user_permissions.permission_manager import UserPermissionManager
from apps.llm_transaction.models import TransactionInvoice, InvoiceTypesNames, PaymentMethodsNames
from apps.organization.models import Organization
from apps.user_permissions.models import PermissionNames


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

        ##############################
        # PERMISSION CHECK FOR - ADD_BALANCE_TO_ORGANIZATION
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.ADD_BALANCE_TO_ORGANIZATION):
            messages.error(self.request, "You do not have permission to add balance to organizations.")
            return redirect('llm_transaction:list')
        ##############################

        organization_id = kwargs.get('pk')
        user = request.user
        print(f"[OrganizationUserAddGiftCreditsView.get] Adding gift credits to organization {organization_id}.")

        org = get_object_or_404(Organization, id=organization_id, users__in=[request.user])
        user = User.objects.get(id=user.id)
        print(f"[OrganizationUserAddGiftCreditsView.get] Adding gift credits to {org.name}.")
        try:
            if user.profile.free_credits != 0:
                free_credits = user.profile.free_credits
                print(
                    f"[OrganizationUserAddGiftCreditsView.get] Available gift credits: {free_credits} for user '{user.username}'.")
                user.profile.free_credits = 0
                user.profile.save()
                user.save()
                print(f"[OrganizationUserAddGiftCreditsView.get] Updated user profile and user.")
                org.balance += decimal.Decimal.from_float(free_credits)
                org.save()

                ############################################
                # Create the invoice for the transaction
                TransactionInvoice.objects.create(
                    organization=org,
                    responsible_user=request.user,
                    transaction_type=InvoiceTypesNames.GIFT_CREDITS,
                    amount_added=decimal.Decimal.from_float(free_credits),
                    payment_method=PaymentMethodsNames.INTERNAL_TRANSFER,
                )
                ############################################

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
