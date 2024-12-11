#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: integrate_daily_logs_datasource_prompts.py
#  Last Modified: 2024-10-29 19:34:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-29 19:34:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.metatempo.models import (
    MetaTempoConnection,
    MetaTempoMemberLogDaily
)


def get_daily_logs_datasource_prompt(
    connection: MetaTempoConnection,
    batched_logs: list
):
    daily_logs_prompt = f"""
        -----

        **DAILY LOGS DATA:**

        '''

    """

    for log in batched_logs:
        log: MetaTempoMemberLogDaily

        daily_logs_prompt += f"""
            ---
            [User: {log.user.username if log.user else 'N/A'}]
            [Daily Activity Summary]
                '''
                {log.daily_activity_summary}
                '''
            [Key Tasks]
                '''
                {log.key_tasks}
                '''
            [Overall Work Intensity]
                '''
                {log.overall_work_intensity}
                '''
            [Application Usage Stats]
                '''
                {log.application_usage_stats}
                '''
            [Datestamp: {log.datestamp}]
            [Created At: {log.created_at}]
            ***
            ---
        """

    daily_logs_prompt += f"""
        '''

        -----

        - **NOTE:** The daily logs that are listed here are the daily logs from the Tempo tracker's previous recording
        history. You can use this information to understand the current state of the tempo, performance, efficiency,
        throughput and other useful metrics associated with the project, tasks and overall goals. This information
        can also be used to understand the context of the queries delivered to you in a better way.

        -----
    """

    return daily_logs_prompt
