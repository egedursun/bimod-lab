#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: finetuned_model_forms.py
#  Last Modified: 2024-09-27 18:25:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:53:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django import forms

from apps.finetuning.models import FineTunedModelConnection


class FineTunedModelConnectionForm(forms.ModelForm):
    class Meta:
        model = FineTunedModelConnection
        fields = ['organization', 'nickname', 'model_name', 'model_type', 'provider', 'provider_api_key',
                  'model_description']
