#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: custom_function_reference_forms.py
#  Last Modified: 2024-09-28 16:27:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:01:02
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django import forms

from apps.mm_functions.models import CustomFunctionReference


class CustomFunctionReferenceForm(forms.ModelForm):
    class Meta:
        model = CustomFunctionReference
        fields = ['custom_function', 'assistant']
        widgets = {
            'custom_function': forms.Select(attrs={'class': 'form-control'}),
            'assistant': forms.Select(attrs={'class': 'form-control'}),
        }
