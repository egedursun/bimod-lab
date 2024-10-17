#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: nosql_query_forms.py
#  Last Modified: 2024-10-12 13:16:24
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 13:16:25
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

from apps.datasource_nosql.models import CustomNoSQLQuery


class CustomNoSQLQueryForm(forms.ModelForm):
    class Meta:
        model = CustomNoSQLQuery
        fields = [
            'database_connection', 'name', 'description', 'nosql_query',
        ]
        widgets = {
            'nosql_query': forms.Textarea(attrs={'rows': 10}),
        }
