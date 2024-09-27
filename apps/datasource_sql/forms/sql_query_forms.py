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
