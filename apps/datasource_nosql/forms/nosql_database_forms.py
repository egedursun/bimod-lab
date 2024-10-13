#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: nosql_database_forms.py
#  Last Modified: 2024-10-12 13:16:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-12 13:16:16
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

from apps.datasource_nosql.models import NoSQLDatabaseConnection


class NoSQLDatabaseConnectionForm(forms.ModelForm):
    class Meta:
        model = NoSQLDatabaseConnection
        fields = [
            'assistant', 'nosql_db_type', 'name', 'description', 'host', 'bucket_name', 'username',
            'password', 'is_read_only', 'created_by_user', 'one_time_retrieval_instance_limit',
            'one_time_retrieval_token_limit',
        ]
        widgets = {'password': forms.PasswordInput()}
        exclude = ['schema_data_json']
