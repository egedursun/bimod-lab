
from django import forms
from apps.datasource_sql.models import SQLDatabaseConnection


class SQLDatabaseConnectionForm(forms.ModelForm):
    class Meta:
        model = SQLDatabaseConnection
        fields = [
            'assistant',
            'dbms_type',
            'name',
            'description',
            'host',
            'port',
            'database_name',
            'username',
            'password',
            'is_read_only',
            'created_by_user',
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }
        exclude = ['schema_data_json']
