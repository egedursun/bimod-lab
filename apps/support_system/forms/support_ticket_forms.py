from django import forms

from apps.support_system.models import SupportTicket


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['title', 'issue_description', 'priority', 'attachment']
