#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: triggered_job_forms.py
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
#
#
#

#
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
