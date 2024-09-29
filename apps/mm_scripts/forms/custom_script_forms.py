#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: custom_script_forms.py
#  Last Modified: 2024-09-27 19:28:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:02:59
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django import forms

from apps.mm_scripts.models import CustomScript


class CustomScriptForm(forms.ModelForm):
    class Meta:
        model = CustomScript
        fields = ['name', 'description', 'script_picture', 'categories', 'script_content', 'script_step_guide',
                  'is_public']
        widgets = {
            'script_step_guide': forms.Textarea(attrs={'rows': 5}),
            'script_content': forms.Textarea(attrs={'rows': 10}), 'categories': forms.CheckboxSelectMultiple(),
        }
