from django import forms

from apps.data_security.models import NERIntegration


class NERIntegrationForm(forms.ModelForm):
    class Meta:
        model = NERIntegration
        fields = [
            'organization', 'name', 'description', 'language',
            'encrypt_persons', 'encrypt_orgs', 'encrypt_nationality_religion_political', 'encrypt_facilities',
            'encrypt_countries_cities_states', 'encrypt_locations', 'encrypt_products', 'encrypt_events',
            'encrypt_artworks', 'encrypt_laws', 'encrypt_languages', 'encrypt_dates', 'encrypt_times',
            'encrypt_percentages', 'encrypt_money', 'encrypt_quantities', 'encrypt_ordinal_numbers',
            'encrypt_cardinal_numbers', 'created_by_user'
        ]
        widgets = {
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-select'}),
        }
