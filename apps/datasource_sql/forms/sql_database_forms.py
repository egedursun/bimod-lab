#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: sql_database_forms.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
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

from apps.datasource_sql.models import SQLDatabaseConnection
from django import forms


class SQLDatabaseConnectionForm(forms.ModelForm):
    class Meta:
        model = SQLDatabaseConnection
        fields = [
            'assistant', 'dbms_type', 'name', 'description', 'host', 'port', 'database_name', 'username',
            'password', 'is_read_only', 'created_by_user', 'one_time_sql_retrieval_instance_limit',
            'one_time_sql_retrieval_token_limit',
        ]
        widgets = {'password': forms.PasswordInput()}
        exclude = ['schema_data_json']
