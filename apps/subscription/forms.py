from django import forms

from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = [
            'organization',
            'name_on_card',
            'card_number',
            'card_expiration_month',
            'card_expiration_year',
            'card_cvc',
            'subscription_plan'
        ]
