#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: integrate_overall_logs_datasource_prompts.py
#  Last Modified: 2024-10-29 19:34:49
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-29 19:34:50
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
    MetaTempoProjectOverallLog
)


def get_overall_logs_datasource_prompt(
    connection: MetaTempoConnection,
    batched_logs: list
):
    overall_analysis_logs = f"""
                -----

                **OVERALL ANALYSIS LOG SNAPSHOTS DATA:**

                '''

            """

    for log in batched_logs:
        log: MetaTempoProjectOverallLog

        overall_analysis_logs += f"""
                    ---
                    [Overall Activity Summary]
                        '''
                        {log.overall_activity_summary}
                        '''
                    [Overall Key Insights]
                        '''
                        {log.overall_key_insights}
                        '''
                    [Overall Work Intensity]
                        '''
                        {log.overall_work_intensity}
                        '''
                    [Overall Application Usage Stats]
                        '''
                        {log.overall_application_usage_stats}
                        '''
                    [Datestamp: {log.datestamp}]
                    [Created At: {log.created_at}]
                    ***
                    ---
                """

    overall_analysis_logs += f"""
                '''

                -----

                - **NOTE:** The overall analysis logs that are listed here are the logs from the Tempo tracker's
                previous recording history **FOR ALL TEAMS OF THE PROJECT FOR A TIME PERIOD**. You can use this
                information to understand the current state of the tempo, performance, efficiency, throughput and
                other useful metrics associated with the project, tasks and overall goals. This information can also
                be used to understand the context of the queries delivered to you in a better way.

                -----
            """

    return overall_analysis_logs
