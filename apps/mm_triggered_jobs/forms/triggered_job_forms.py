#  Copyright Policy & Ownership
#
#  Bimod.io is a product of BMD Holdings. All materials, including but not limited to software, code, documentation,
#  graphics, design elements, and user interfaces provided by Bimod.io are protected by copyright law and international
#  treaties.
#  All content within Bimod.io is the exclusive property of BMD Holdings, unless otherwise stated.
#  Unauthorized use, distribution, or reproduction of any material contained in this software without the express
#  written consent of BMD Holdings is strictly prohibited.
#  Users may not copy, modify, distribute, display, perform, or create derivative works of Bimod.io without prior
#  written permission from BMD Holdings.

from django import forms

from apps.mm_triggered_jobs.models import TriggeredJob


class TriggeredJobForm(forms.ModelForm):
    class Meta:
        model = TriggeredJob
        fields = ['name', 'task_description', 'step_guide', 'trigger_assistant', 'trigger_source', 'event_type',
                  'maximum_runs']
        widgets = {'step_guide': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, **kwargs):
        super(TriggeredJobForm, self).__init__(*args, **kwargs)
        self.fields['step_guide'].required = False

    def clean(self):
        cleaned_data = super(TriggeredJobForm, self).clean()
        return cleaned_data
