from django import forms

from apps.mm_functions.models import CustomFunction, CustomFunctionReference


class CustomFunctionForm(forms.ModelForm):
    class Meta:
        model = CustomFunction
        fields = ['name', 'description', 'packages', 'input_fields', 'output_fields', 'code_text', 'is_public',
                  'function_picture', 'created_by_user']


class CustomFunctionReferenceForm(forms.ModelForm):
    class Meta:
        model = CustomFunctionReference
        fields = ['custom_function', 'assistant']
        widgets = {
            'custom_function': forms.Select(attrs={'class': 'form-control'}),
            'assistant': forms.Select(attrs={'class': 'form-control'}),
        }
