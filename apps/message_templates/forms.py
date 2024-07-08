
from django import forms
from .models import MessageTemplate


class MessageTemplateForm(forms.ModelForm):
    class Meta:
        model = MessageTemplate
        fields = ['organization', 'template_text']
        widgets = {
            'template_text': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }
