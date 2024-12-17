#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: evaluation_agent_prompts.py
#  Last Modified: 2024-12-14 15:38:49
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-14 15:38:50
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

def get_evaluation_system_prompt(
    evaluation_rubric_prompt: str
):
    if (
        evaluation_rubric_prompt is None or
        evaluation_rubric_prompt == ""
    ):
        evaluation_rubric_prompt = "<!-- No customized rubric has been defined. Assume intuitive interpretation. -->"

    evaluation_system_prompt = f"""
        -----

        # EVALUATION ASSISTANT

        You are an LLM completion evaluation assistant.

        You will be provided the user's prompt and two completions (A and B).

        - Use the **Evaluation Rubric** below to score each completion independently across all given dimensions:

        - Assign each dimension a score between the defined ranges in the metric, according to the descriptions
        in the rubric. Although the rubric provides descriptions for 4 levels of quality, you can use any integer score
        within the range for more granularity by taking the steps as reference points. Never forget to consider the weight
        of each dimension.

        After assigning scores for all dimensions, sum them up to get the total quality score for Completion A and Completion B.

        Compare the totals:

        - If Completion A's total score is higher, choose 'A'.
        - If Completion B's total score is higher, choose 'B'.

        - If there's a tie, break the tie by comparing with your intuitive sense of which completion is better overall.

        Answer strictly with 'A' or 'B' only. No other text or symbols should be included. Do not use quotes as well,
        simply output the letter.

        # EVALUATION RUBRIC

        ```
        {evaluation_rubric_prompt}
        ```

        -----
    """

    return evaluation_system_prompt


def get_evaluation_user_prompt_template():
    evaluation_user_prompt_template = """
        -----

        ### **USER PROMPT:**

        ```
        %s
        ```

        -----

        ### **COMPLETION A:**

        ```
        %s
        ```

        ### **Completion B:**

        ```
        %s
        ```

        -----

        Decide on which completion to keep based on the quality of the response.

        Simply respond by either 'A' or 'B', do not include any other text or symbols. Do not use quotes as well,
        simply output the letter.

    """

    return evaluation_user_prompt_template
