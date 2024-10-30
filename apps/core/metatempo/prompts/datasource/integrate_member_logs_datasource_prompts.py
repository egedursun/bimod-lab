#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: integrate_member_logs_datasource_prompts.py
#  Last Modified: 2024-10-29 19:34:29
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-29 19:34:30
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from apps.metatempo.models import MetaTempoConnection, MetaTempoMemberLog


def get_member_logs_datasource_prompt(connection: MetaTempoConnection, batched_logs: list):
    member_snapshot_logs_prompt = f"""
            -----

            **MEMBER SNAPSHOTS DATA:**

            '''

        """

    for log in batched_logs:
        log: MetaTempoMemberLog
        member_snapshot_logs_prompt += f"""
                ---
                [User: {log.user.username if log.user else 'N/A'}]
                [Screenshot Image]
                    '''
                    < Shared in the user message within the conversation >
                    '''
                [Activity Summary]
                    '''
                    {log.activity_summary}
                    '''
                [Activity Tags]
                    '''
                    {log.activity_tags}
                    '''
                [Work Intensity]
                    '''
                    {log.work_intensity}
                    '''
                [Application Usage Stats]
                    '''
                    {log.application_usage_stats}
                    '''
                [Timestamp: {log.timestamp}]
                ***
                ---
            """

    member_snapshot_logs_prompt += f"""
            '''

            -----

            - **NOTE:** The member logs that are listed here are the logs from the Tempo tracker's previous recording
            history **DURING A WORK DAY**. You can use this information to understand the current state of the tempo,
            performance, efficiency, throughput and other useful metrics associated with the project, tasks and overall
            goals. This information can also be used to understand the context of the queries delivered to you in a
            better way.

            -----
        """

    return member_snapshot_logs_prompt
