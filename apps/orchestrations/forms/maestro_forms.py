#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: maestro_forms.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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

from apps.llm_core.models import LLMCore
from apps.orchestrations.models import Maestro
from apps.organization.models import Organization


class MaestroForm(forms.ModelForm):
    organization = forms.ModelChoiceField(queryset=Organization.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
    }))
    llm_model = forms.ModelChoiceField(queryset=LLMCore.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
    }))

    class Meta:
        model = Maestro
        fields = [
            'organization',
            'llm_model',
            'name',
            'description',
            'instructions',
            'workflow_step_guide',
            'maximum_assistant_limits',
            'response_template',
            'audience',
            'tone',
            'response_language',
            'maestro_image',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the name of your orchestration',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the description of your orchestration',
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter instructions for the orchestration',
            }),
            'workflow_step_guide': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the workflow step guide',
            }),
            'maximum_assistant_limits': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the maximum assistant limits',
                'value': 10
            }),
            'response_template': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the response template',
            }),
            'audience': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the target audience of your orchestration',
            }),
            'tone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the tone to be used in responses',
            }),
            'response_language': forms.Select(attrs={
                'class': 'form-control select2',
            }),
            'maestro_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
