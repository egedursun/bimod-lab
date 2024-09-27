from django import forms

from auth.models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'birthdate',
                  'address', 'city', 'country', 'postal_code', 'profile_picture']
