#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: ml_model_storage_forms.py
#  Last Modified: 2024-09-28 23:19:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: ml_model_storage_forms.py
#  Last Modified: 2024-09-27 23:54:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:47:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django import forms

from apps.datasource_ml_models.models import DataSourceMLModelConnection


class DataSourceMLModelConnectionForm(forms.ModelForm):
    class Meta:
        model = DataSourceMLModelConnection
        fields = [
            'assistant', 'name', 'description', 'model_object_category', 'directory_schema',
            'interpretation_temperature', 'interpretation_maximum_tokens'
        ]
        widgets = {
            'assistant': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter data source name'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Enter data source description', 'rows': 3
            }),
            'model_object_category': forms.Select(attrs={'class': 'form-select'}),
            'interpretation_temperature': forms.NumberInput(attrs={'class': 'form-control'}),
            'interpretation_maximum_tokens': forms.NumberInput(attrs={'class': 'form-control'}),
        }
