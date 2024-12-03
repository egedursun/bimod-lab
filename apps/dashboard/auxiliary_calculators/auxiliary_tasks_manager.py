#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auxiliary_tasks_manager.py
#  Last Modified: 2024-10-09 21:48:16
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 21:48:17
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.utils import timezone

from apps.mm_scheduled_jobs.models import (
    ScheduledJobInstance
)

from apps.mm_triggered_jobs.models import (
    TriggeredJobInstance
)


class AuxiliaryTasksManager:

    @staticmethod
    def calculate_total_triggered_jobs_per_assistants(
        agents,
        trg_jobs,
        n_days
    ):

        result = {}

        for a in agents:
            a_jobs = 0
            for jb in trg_jobs:
                trg_insts = TriggeredJobInstance.objects.filter(
                    triggered_job=jb,
                    started_at__gte=timezone.now() - timezone.timedelta(
                        days=n_days
                    )
                )
                a_jobs += trg_insts.count()

            result[a.name] = a_jobs

        return result

    @staticmethod
    def calculate_total_scheduled_jobs_per_assistants(
        agents,
        sched_jobs,
        n_days
    ):

        result = {}

        for a in agents:

            a_jobs = 0

            for jb in sched_jobs:
                sched_insts = ScheduledJobInstance.objects.filter(
                    scheduled_job=jb,
                    started_at__gte=timezone.now() - timezone.timedelta(
                        days=n_days
                    )
                )

                a_jobs += sched_insts.count()

            result[a.name] = a_jobs

        return result
