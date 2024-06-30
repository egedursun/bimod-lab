

from django import forms
from .models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            'name',
            'email',
            'phone',
            'address',
            'city',
            'country',
            'postal_code',
            'industry',
            'organization_image',
        ]
