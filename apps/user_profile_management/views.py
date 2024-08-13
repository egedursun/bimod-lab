"""
Module for managing user profiles within the web application.

This module contains views that allow users to manage their profile details, credit card information, and password reset functionality. The module ensures that users can securely update their personal information and manage their stored credit cards.

Views:
    - UserProfileListView: Displays the user's profile details and credit card information, allowing updates to both.
    - UserProfileResetPasswordView: Sends a password reset email to the user.
    - RemoveCardView: Handles the removal of a user's stored credit card.

Forms:
    - ProfileUpdateForm: Used for updating user profile details.
    - CreditCardForm: Used for adding and updating credit card information.

Utilities:
    - get_card_type: Determines the type of credit card based on the card number.
    - send_password_reset_email: Sends a password reset email to the user.

Models:
    - User: Django's built-in user model.
    - UserCreditCard: Represents a user's credit card information.
    - Profile: Represents additional user profile information.
"""

import uuid

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.user_profile_management.forms import ProfileUpdateForm, CreditCardForm
from apps.user_profile_management.utils import get_card_type
from auth.countries import COUNTRIES
from auth.helpers import send_password_reset_email
from auth.models import UserCreditCard
from config import settings
from web_project import TemplateLayout


# Create your views here.
class UserProfileListView(LoginRequiredMixin, TemplateView):
    """
    Displays the user's profile information and credit cards.

    GET:
    - Renders the user's profile and associated credit cards.
    - Provides forms for updating profile information and adding new credit cards.

    POST:
    - Handles profile updates and credit card additions.
    - Validates the submitted forms and saves the changes.
    - Displays success or error messages based on the operation outcome.
    """
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['countries'] = COUNTRIES
        context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        context['credit_card_form'] = CreditCardForm()
        saved_cards = self.request.user.credit_cards.all()
        cards_with_types = []
        for card in saved_cards:
            card_type = get_card_type(card.card_number)
            cards_with_types.append({'card': card, 'card_type': card_type})
        context['saved_cards'] = cards_with_types
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        profile = request.user.profile
        if 'first_name' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                print('[UserProfileListView.post] Profile updated successfully.')
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('user_profile_management:list')
            else:
                messages.error(request, 'Please correct the error(s) below.')
            context = self.get_context_data()
            context['profile_form'] = profile_form
        elif 'card_number' in request.POST:
            credit_card_form = CreditCardForm(request.POST)
            if credit_card_form.is_valid():
                credit_card = credit_card_form.save(commit=False)
                credit_card.user = request.user
                credit_card.save()
                print('[UserProfileListView.post] Credit card updated successfully.')
                messages.success(request, 'Your credit card was successfully updated!')
                return redirect('user_profile_management:list')
            else:
                messages.error(request, 'Please correct the error(s) below.')
            context['credit_card_form'] = credit_card_form
        return self.render_to_response(context)


class UserProfileResetPasswordView(LoginRequiredMixin, TemplateView):
    """
    Sends a password reset email to the user.

    GET:
    - Fetches the user based on the provided primary key (pk).
    - Generates a password reset token and sends a reset email to the user's email address.
    - Displays success or error messages depending on the email sending status.
    """
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['pk'] = self.kwargs.get('pk')
        print('[UserProfileResetPasswordView.get_context_data] PK:', context['pk'])
        return context

    def get(self, request, *args, **kwargs):
        pk = self.get_context_data()['pk']
        try:
            user = User.objects.get(pk=pk)
            email = user.email
            token = str(uuid.uuid4())
            send_password_reset_email(email, token)
            if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                print('[UserProfileResetPasswordView.get] Password reset email sent successfully!')
                messages.success(request, 'Password reset email sent successfully!')
            else:
                print('[UserProfileResetPasswordView.get] Email settings are not configured. Unable to send verification email.')
                messages.error(request, 'Email settings are not configured. Unable to send verification email.')
            print('[UserProfileResetPasswordView.get] Password reset email sent successfully.')
            messages.success(request, 'Password reset email sent successfully!')
        except Exception as e:
            messages.error(request, f'Failed to send password reset email: {e}')
        print('[UserProfileResetPasswordView.get] Password reset email sent successfully.')
        return self.render_to_response(self.get_context_data())


class RemoveCardView(LoginRequiredMixin, TemplateView):
    """
    Handles the removal of a user's stored credit card.

    POST:
    - Deletes the specified credit card from the user's account.
    - Displays a success message if the card is removed successfully.
    - Displays an error message if the specified card does not exist.
    """
    def post(self, request, card_id, *args, **kwargs):
        try:
            card = request.user.credit_cards.get(id=card_id)
            card.delete()
            print('[RemoveCardView.post] Credit card removed successfully.')
            messages.success(request, 'Credit card removed successfully.')
        except UserCreditCard.DoesNotExist:
            messages.error(request, 'Credit card not found.')
        return redirect('user_profile_management:list')
