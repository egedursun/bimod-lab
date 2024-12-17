#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: user_role_forms.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
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

from apps.user_permissions.models import (
    UserRole
)

from apps.user_permissions.utils import (
    PERMISSION_TYPES
)


class UserRoleForm(forms.ModelForm):
    role_permissions = forms.MultipleChoiceField(
        choices=PERMISSION_TYPES,
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-select',
                'multiple': 'multiple'
            }
        ),
        required=True
    )

    class Meta:
        model = UserRole
        fields = [
            'organization',
            'role_name',
            'role_description',
            'role_permissions'
        ]
