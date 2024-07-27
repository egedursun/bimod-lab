from django import forms

from apps.mm_apis.models import CustomAPI


class CustomAPIForm(forms.ModelForm):
    class Meta:
        model = CustomAPI
        fields = [
            'name',
            'description',
            'api_picture',
            'authentication_type',
            'authentication_token',
            'base_url',
            'categories',
            'is_public'
        ]
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
        }
