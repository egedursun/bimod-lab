from django import forms

from apps.mm_scheduled_jobs.models import ScheduledJob


class ScheduledJobForm(forms.ModelForm):
    class Meta:
        model = ScheduledJob
        fields = ['name', 'task_description', 'step_guide', 'assistant', 'minute',
                  'hour', 'day_of_week', 'day_of_month', 'month_of_year', 'maximum_runs']
        widgets = {
            'step_guide': forms.Textarea(attrs={'rows': 5}),
            'task_description': forms.Textarea(attrs={'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super(ScheduledJobForm, self).__init__(*args, **kwargs)
        self.fields['step_guide'].required = False

    def clean(self):
        cleaned_data = super(ScheduledJobForm, self).clean()

        minute = cleaned_data.get('minute')
        hour = cleaned_data.get('hour')
        day_of_week = cleaned_data.get('day_of_week')
        day_of_month = cleaned_data.get('day_of_month')
        month_of_year = cleaned_data.get('month_of_year')
        if not (minute and hour and day_of_week and day_of_month and month_of_year):
            raise forms.ValidationError("All cron fields are required for chronological jobs.")

        return cleaned_data
