#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metakanban_meeting_records_datasource_prompt.py
#  Last Modified: 2024-11-14 04:54:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-14 04:54:28
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from apps.metakanban.models import (
    MetaKanbanBoard,
    MetaKanbanMeetingTranscription
)

logger = logging.getLogger(__name__)


def get_latest_meeting_transcriptions_prompt(board: MetaKanbanBoard):
    prompt = f"""
        -----

        ### **BOARD / LATEST MEETING TRANSCRIPTIONS:**

        -----
    """

    for tsc in board.metakanbanmeetingtranscription_set.filter(is_processed_with_ai=False).order_by('-created_at')[:5]:
        tsc: MetaKanbanMeetingTranscription
        prompt += f"""

        [Meeting Transcription ID: {tsc.id}]
            [Meeting Transcription Text: {tsc.meeting_transcription_text}]
            [Meeting Key Takeaways: {tsc.meeting_transcription_key_takeaways}]
        ---
        ***
        """

    prompt += """

        -----

        - **NOTE:** The above meeting transcriptions are the latest 5 meeting transcriptions for the board. If prompted
        by the user, you can integrate the updates requested/mentioned in the meeting transcriptions to the MetaKanban
        boards by using the associated actions. This requires the user to prompt it openly to you. For example, if the user
        tells you to "update the board based on the last meetings", you can use the actions in your action_types stack
        to perform the necessary changes/manipulations on the MetaKanban Board.
    """

    return prompt
