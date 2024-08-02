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
