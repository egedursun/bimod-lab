from django import forms

from .models import Subscription, SUBSCRIPTION_PLANS


class SubscriptionForm(forms.ModelForm):
    subscription_plan = forms.ChoiceField(choices=SUBSCRIPTION_PLANS)
    subscription_period = forms.ChoiceField(choices=[('monthly', 'Monthly'), ('annual', 'Annual')])

    class Meta:
        model = Subscription
        fields = [
            'organization',
            'name_on_card',
            'card_number',
            'card_expiration_month',
            'card_expiration_year',
            'card_cvc',
            'subscription_plan',
        ]
