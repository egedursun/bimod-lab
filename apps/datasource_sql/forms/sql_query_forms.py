#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: sql_query_forms.py
#  Last Modified: 2024-09-27 17:48:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:48:52
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django import forms

from apps.datasource_sql.models import CustomSQLQuery


class CustomSQLQueryForm(forms.ModelForm):
    class Meta:
        model = CustomSQLQuery
        fields = [
            'database_connection', 'name', 'description', 'sql_query',
        ]
        widgets = {
            'sql_query': forms.Textarea(attrs={'rows': 10}),
        }
