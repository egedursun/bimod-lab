from django import forms

from auth.models import Profile, UserCreditCard


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'birthdate',
                  'address', 'city', 'country', 'postal_code', 'profile_picture']


class CreditCardForm(forms.ModelForm):
    class Meta:
        model = UserCreditCard
        fields = ['name_on_card', 'card_number', 'card_expiration_month', 'card_expiration_year', 'card_cvc']
