from django import forms

from auth.models import UserCreditCard


class CreditCardForm(forms.ModelForm):
    class Meta:
        model = UserCreditCard
        fields = ['name_on_card', 'card_number', 'card_expiration_month', 'card_expiration_year', 'card_cvc']
