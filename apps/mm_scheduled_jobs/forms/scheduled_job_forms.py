#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: scheduled_job_forms.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django import forms

from apps.mm_scheduled_jobs.models import (
    ScheduledJob
)


class ScheduledJobForm(forms.ModelForm):
    class Meta:
        model = ScheduledJob

        fields = [
            'name',
            'task_description',
            'step_guide',
            'minute',
            'hour', 'day_of_week',
            'day_of_month',
            'month_of_year',
            'maximum_runs'
        ]

        widgets = {
            'step_guide': forms.Textarea(
                attrs={
                    'rows': 5
                }
            ),
            'task_description': forms.Textarea(
                attrs={
                    'rows': 10
                }
            ),
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

    if not (
        minute and
        hour and
        day_of_week and
        day_of_month and
        month_of_year
    ):
        raise forms.ValidationError("All cron fields are required for chronological jobs.")

    return cleaned_data
