from django import forms

from apps.finetuning.models import FineTunedModelConnection


class FineTunedModelConnectionForm(forms.ModelForm):
    class Meta:
        model = FineTunedModelConnection
        fields = ['organization', 'nickname', 'model_name', 'model_type', 'provider', 'provider_api_key',
                  'model_description']
