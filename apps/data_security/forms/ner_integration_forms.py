#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ner_integration_forms.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django import forms

from apps.data_security.models import (
    NERIntegration
)


class NERIntegrationForm(forms.ModelForm):
    class Meta:
        model = NERIntegration
        fields = [
            'organization',
            'name',
            'description',
            'language',
            'encrypt_persons',
            'encrypt_orgs',
            'encrypt_nationality_religion_political',
            'encrypt_facilities',
            'encrypt_countries_cities_states',
            'encrypt_locations',
            'encrypt_products',
            'encrypt_events',
            'encrypt_artworks',
            'encrypt_laws',
            'encrypt_languages',
            'encrypt_dates',
            'encrypt_times',
            'encrypt_percentages',
            'encrypt_money',
            'encrypt_quantities',
            'encrypt_ordinal_numbers',
            'encrypt_cardinal_numbers',
            'created_by_user'
        ]

        widgets = {
            'organization': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'language': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }
