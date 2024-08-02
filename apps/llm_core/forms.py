from django import forms
from .models import LLMCore


class LLMCoreForm(forms.ModelForm):
    class Meta:
        model = LLMCore
        fields = [
            'nickname', 'description', 'provider', 'api_key', 'model_name', 'temperature', 'maximum_tokens',
            'stop_sequences', 'top_p', 'frequency_penalty', 'presence_penalty', 'organization',
        ]
