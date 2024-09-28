from django import forms

from apps.mm_functions.models import CustomFunctionReference


class CustomFunctionReferenceForm(forms.ModelForm):
    class Meta:
        model = CustomFunctionReference
        fields = ['custom_function', 'assistant']
        widgets = {
            'custom_function': forms.Select(attrs={'class': 'form-control'}),
            'assistant': forms.Select(attrs={'class': 'form-control'}),
        }
