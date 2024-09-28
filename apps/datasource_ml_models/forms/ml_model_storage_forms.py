from django import forms

from apps.datasource_ml_models.models import DataSourceMLModelConnection


class DataSourceMLModelConnectionForm(forms.ModelForm):
    class Meta:
        model = DataSourceMLModelConnection
        fields = [
            'assistant', 'name', 'description', 'model_object_category', 'directory_schema',
            'interpretation_temperature', 'interpretation_maximum_tokens'
        ]
        widgets = {
            'assistant': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter data source name'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Enter data source description', 'rows': 3
            }),
            'model_object_category': forms.Select(attrs={'class': 'form-select'}),
            'interpretation_temperature': forms.NumberInput(attrs={'class': 'form-control'}),
            'interpretation_maximum_tokens': forms.NumberInput(attrs={'class': 'form-control'}),
        }
