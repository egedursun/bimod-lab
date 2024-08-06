from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.user_profile_management.forms import ProfileUpdateForm, CreditCardForm
from apps.user_profile_management.utils import get_card_type
from auth.countries import COUNTRIES
from auth.models import UserCreditCard
from web_project import TemplateLayout


# Create your views here.
class UserProfileListView(LoginRequiredMixin, TemplateView):
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


class RemoveCardView(LoginRequiredMixin, TemplateView):
    def post(self, request, card_id, *args, **kwargs):
        try:
            card = request.user.credit_cards.get(id=card_id)
            card.delete()
            print('[RemoveCardView.post] Credit card removed successfully.')
            messages.success(request, 'Credit card removed successfully.')
        except UserCreditCard.DoesNotExist:
            messages.error(request, 'Credit card not found.')
        return redirect('user_profile_management:list')
