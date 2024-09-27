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
