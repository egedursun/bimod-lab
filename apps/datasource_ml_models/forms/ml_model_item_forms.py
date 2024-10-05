#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: ml_model_item_forms.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

from django import forms

from apps.datasource_ml_models.models import DataSourceMLModelItem


class DataSourceMLModelItemForm(forms.ModelForm):
    file = forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = DataSourceMLModelItem
        fields = ['ml_model_base', 'ml_model_name', 'description', 'interpretation_temperature']
        widgets = {
            'ml_model_base': forms.Select(attrs={'class': 'form-select'}),
            'ml_model_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ML model name'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Enter description for the ML model', 'rows': 3
            }),
        }
