from django import forms

from apps.mm_functions.models import CustomFunction


class CustomFunctionForm(forms.ModelForm):
    class Meta:
        model = CustomFunction
        fields = ['name', 'description', 'packages', 'input_fields', 'output_fields', 'code_text', 'is_public',
                  'function_picture', 'created_by_user']
