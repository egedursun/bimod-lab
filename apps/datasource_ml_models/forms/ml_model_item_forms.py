from django import forms

from apps.datasource_ml_models.models import DataSourceMLModelItem


class DataSourceMLModelItemForm(forms.ModelForm):
    file = forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = DataSourceMLModelItem
        fields = ['ml_model_base', 'ml_model_name', 'description', 'interpretation_temperature']
        widgets = {
            'ml_model_base': forms.Select(attrs={'class': 'form-select'}),
            'ml_model_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ML model name'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Enter description for the ML model', 'rows': 3
            }),
        }
