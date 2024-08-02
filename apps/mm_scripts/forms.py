from django import forms

from apps.mm_scripts.models import CustomScript


class CustomScriptForm(forms.ModelForm):
    class Meta:
        model = CustomScript
        fields = ['name', 'description', 'script_picture', 'categories', 'script_content', 'script_step_guide', 'is_public']
        widgets = {
            'script_step_guide': forms.Textarea(attrs={'rows': 5}),
            'script_content': forms.Textarea(attrs={'rows': 10}), 'categories': forms.CheckboxSelectMultiple(),
        }
