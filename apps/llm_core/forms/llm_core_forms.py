#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: llm_core_forms.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django import forms

from apps.llm_core.models import LLMCore


class LLMCoreForm(forms.ModelForm):
    class Meta:
        model = LLMCore
        fields = [
            'nickname', 'description', 'provider', 'api_key', 'model_name', 'temperature', 'maximum_tokens',
            'stop_sequences', 'top_p', 'frequency_penalty', 'presence_penalty', 'organization',
        ]

    def clean_model_name(self):
        # Bypass the choices validation
        return self.cleaned_data.get('model_name')
