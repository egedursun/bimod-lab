from django import forms
from .models import LLMCore, OPENAI_GPT_MODEL_NAMES


class LLMCoreForm(forms.ModelForm):

    class Meta:
        model = LLMCore
        fields = [
            'nickname', 'description', 'provider', 'api_key', 'model_name', 'temperature', 'maximum_tokens',
            'stop_sequences', 'top_p', 'frequency_penalty', 'presence_penalty', 'organization',
        ]

    def clean_model_name(self):
        # Bypass the choices validation
        return self.cleaned_data.get('model_name')
