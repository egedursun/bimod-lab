from django import forms


"""
class SubscriptionForm(forms.ModelForm):
    subscription_plan = forms.ChoiceField(choices=SUBSCRIPTION_PLANS)
    subscription_period = forms.ChoiceField(choices=[('monthly', 'Monthly'), ('annual', 'Annual')])

    class Meta:
        model = Subscription
        fields = [
            'user',
            # 'credit_card',
            'subscription_plan',
            'subscription_start_date',
            'subscription_end_date',
            'auto_renew',
            'auto_renew_mode',
        ]

"""
