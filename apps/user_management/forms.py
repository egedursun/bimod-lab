

from django import forms
from auth.models import Profile


class UserStatusForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['is_active']
        widgets = {'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})}
