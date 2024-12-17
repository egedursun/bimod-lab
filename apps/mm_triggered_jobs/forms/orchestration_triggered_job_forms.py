#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: orchestration_triggered_job_forms.py
#  Last Modified: 2024-11-14 07:19:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-14 07:19:41
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

from apps.mm_triggered_jobs.models import (
    OrchestrationTriggeredJob
)


class OrchestrationTriggeredJobForm(forms.ModelForm):
    class Meta:
        model = OrchestrationTriggeredJob
        fields = [
            'name',
            'task_description',
            'step_guide',
            'trigger_source',
            'event_type',
            'maximum_runs'
        ]
        widgets = {
            'step_guide': forms.Textarea(
                attrs={
                    'rows': 3
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(OrchestrationTriggeredJobForm, self).__init__(*args, **kwargs)

        self.fields['step_guide'].required = False

    def clean(self):
        cleaned_data = super(OrchestrationTriggeredJobForm, self).clean()

        return cleaned_data
