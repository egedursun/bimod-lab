

from django import forms
from .models import NoSQLDatabaseConnection, CustomNoSQLQuery


class NoSQLDatabaseConnectionForm(forms.ModelForm):
    class Meta:
        model = NoSQLDatabaseConnection
        fields = [
            'assistant', 'dbms_type', 'name', 'description', 'db_name',
            'host', 'username', 'password', 'is_read_only'
        ]
        widgets = {
            'password': forms.PasswordInput(),
            'description': forms.Textarea(attrs={'rows': 3}),
            'host': forms.TextInput(attrs={'placeholder': 'Enter MongoDB host'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter connection name'}),
            'db_name': forms.TextInput(attrs={'placeholder': 'Enter database name'}),
        }
        labels = {
            'dbms_type': 'Database Type',
            'name': 'Connection Name',
            'db_name': 'Database Name',
            'description': 'Description',
            'host': 'Host',
            'username': 'Username',
            'password': 'Password',
            'is_read_only': 'Read Only',
        }


class CustomNoSQLQueryForm(forms.ModelForm):
    class Meta:
        model = CustomNoSQLQuery
        fields = [
            'database_connection', 'name', 'description',
            'query'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'query': forms.Textarea(attrs={'rows': 5}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter query name'}),
        }
        labels = {
            'database_connection': 'Database Connection',
            'name': 'Query Name',
            'description': 'Description',
            'query': 'Query',
        }
