#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: custom_api_forms.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
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
            'categories': forms.CheckboxSelectMultiple()
        }
