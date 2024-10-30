#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: connection_metadata_prompts.py
#  Last Modified: 2024-10-29 20:49:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-29 20:49:04
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.metatempo.models import MetaTempoConnection


def get_connection_metadata_prompt(connection: MetaTempoConnection):
    connection_metadata_prompt = f"""
        -----

        ### **TEMPO TOOL CONNECTION METADATA:**

        -----
        [Connection ID: {connection.id}]
        [Is Tracking Active]: {connection.is_tracking_active}]
        [Overall Log Intervals]: {connection.overall_log_intervals}]
        [Member Log Intervals]: {connection.member_log_intervals}]
        [Tracked Weekdays]: {connection.tracked_weekdays}]
        [Tracking Start Time]: {connection.tracking_start_time}]
        [Tracking End Time]: {connection.tracking_end_time}]
        ***
        '''

        -----

        - **NOTE:** The connection metadata shown here are the tempo tracker (team and project efficiency, performance,
        throughput etc. metrics tracker) you are managing the team performance & efficiency of. You can use this
        information to understand the current state of the team and the tempo of the team, and the parameters of the
        tracking within the connection to help you have more context about the project and teams.

        -----

    """

    return connection_metadata_prompt
