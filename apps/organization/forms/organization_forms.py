from django import forms

from apps.organization.models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            'name', 'email', 'phone', 'address', 'city', 'country', 'postal_code', 'industry', 'organization_image',
        ]
        exclude = ['created_by_user', 'last_updated_by_user', 'users']
