#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: improvement_agent_prompts.py
#  Last Modified: 2024-12-14 15:38:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-14 15:38:42
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def get_improvement_system_prompt(
    evaluation_rubric_prompt: str
):
    if (
        evaluation_rubric_prompt is None or
        evaluation_rubric_prompt == ""
    ):
        evaluation_rubric_prompt = "<!-- No customized rubric has been defined. Assume intuitive interpretation. -->"

    improvement_system_prompt = f"""

        -----

        # IMPROVEMENT ASSISTANT

        You are an improvement assistant. You will be provided the original user prompt and a completion.

        Your goal is to produce improved completions that score as high as possible across all dimensions outlined
        in the **Evaluation Rubric**. Never forget to consider the weight of each dimension.

        - Carefully review the original completion and then produce a new, enhanced completion that addresses the user's
        request more effectively, correcting errors, filling in omissions, improving clarity, maintaining relevance and
        accuracy, and ensuring a natural, human-like tone, and following other important aspects of the rubric to achieve
        the best possible score.

        - Your improved completion should strive for the highest possible scores according to the rubric.

        -----

        # EVALUATION RUBRIC

        ```
        {evaluation_rubric_prompt}
        ```

        -----
    """

    return improvement_system_prompt


def get_improvement_user_prompt(
    chat_conversation_history: list,
    completion_to_improve: str
):
    improvement_user_prompt = f"""

        ### **CHAT CONVERSATION HISTORY

        ```
        {chat_conversation_history}
        ```

        -----

        ### **ORIGINAL COMPLETION (COMPLETION TO IMPROVE):**

        ```
        {completion_to_improve}
        ```

        # GOAL

        Improve the completion to make it fit better to the user prompt and achieve higher scores across all dimensions
        based on the rubric that is shared with you.

        - You must aim for the highest possible quality score in your improved completion based on the rubric.

        -----
    """

    return improvement_user_prompt
