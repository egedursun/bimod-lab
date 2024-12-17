#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: rubric_prompts.py
#  Last Modified: 2024-12-14 17:57:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-14 17:57:15
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.sinaptera.models import (
    SinapteraConfiguration
)


class RubricWeights:
    COMPREHENSIVENESS = 10
    ACCURACY = 8
    RELEVANCY = 8
    COHESIVENESS = 8
    DILIGENCE = 6
    GRAMMAR = 4  #
    NATURALNESS = 2


def get_evaluation_rubric_prompt(
    sinaptera_configuration: SinapteraConfiguration
):
    user_defined_metrics_list = sinaptera_configuration.additional_rubric_criteria

    user_defined_criteria = []

    for criterion_data_dict in user_defined_metrics_list:
        criterion_name = criterion_data_dict.get("name", None)
        if criterion_name is None:
            continue

        criterion_weight = criterion_data_dict.get("weight", None)
        if criterion_weight is None:
            continue

        criterion_description_3x = criterion_data_dict.get("score_3x_description", "")
        criterion_description_2x = criterion_data_dict.get("score_2x_description", "")
        criterion_description_1x = criterion_data_dict.get("score_1x_description", "")
        criterion_description_0x = criterion_data_dict.get("score_0x_description", "")

        criterion_data_formatted = f"""
            ..........
            **{criterion_name} ({criterion_weight * 3} to 0):**
               - {criterion_weight * 3}: {criterion_description_3x}
               - {criterion_weight * 2}: {criterion_description_2x}
               - {criterion_weight * 1}: {criterion_description_1x}
               - 0: {criterion_description_0x}
            ..........
        """

        user_defined_criteria.append(criterion_data_formatted)

    evaluation_rubric = f"""

    -----

    - Each dimension is scored from N_i to 0, with 2 steps in between, where N_i is the highest score for that dimension,
    and 0 is the lowest score.

    - For each of the steps there are descriptions provided, however, as long as the score is within the range and is an
    integer, it is acceptable to use any score within that range. The steps are defined purely as a guideline and reference
    point to better estimate the quality of the output.

    - A higher score always indicates better quality, while a lower score indicates lower quality.

    1. **Grammar ({RubricWeights.GRAMMAR * 3} to 0):**
       - {RubricWeights.GRAMMAR * 3}: Virtually free of grammatical errors; sentences well-formed and natural.
       - {RubricWeights.GRAMMAR * 2}: Minor grammatical issues that are not impeding understanding.
       - {RubricWeights.GRAMMAR * 1}: Noticeable errors that might distract or cause confusion.
       - 0: Severe errors making it difficult or nearly impossible to understand.

    2. **Comprehensiveness ({RubricWeights.COMPREHENSIVENESS * 3} to 0):**
       - {RubricWeights.COMPREHENSIVENESS * 3}: Thoroughly addresses all or nearly all points of the request and instructions.
       - {RubricWeights.COMPREHENSIVENESS * 2}: Addresses most points in the instructions and user prompt reasonably well, but may omit minor details.
       - {RubricWeights.COMPREHENSIVENESS * 1}: Covers some parts of the instructions and user request, but omits several important details.
       - 0: Barely addresses the instructions and user request’s main points and fails to deliver a useful output.

    3. **Diligence ({RubricWeights.DILIGENCE * 3} to 0)**:
       - {RubricWeights.DILIGENCE * 3}: Shows high effort in satisfying the user's request, includes all required elements, no unjustified omissions.
       - {RubricWeights.DILIGENCE * 2}: Generally diligent, but may omit minor details without affecting the overall quality.
       - {RubricWeights.DILIGENCE * 1}: Noticeable omissions that might be annoying, or signs of reluctance to help the user.
       - 0: Consistently avoids instructions or deviates from them, omits significant amount or quality of requested content.

    4. **Relevancy ({RubricWeights.RELEVANCY * 3} to 0):**
       - {RubricWeights.RELEVANCY * 3}: Highly relevant and focused, no off-topic content is being included to the content.
       - {RubricWeights.RELEVANCY * 2}: Mostly relevant based on the user's request and instructions, but there are minor irrelevancies.
       - {RubricWeights.RELEVANCY * 1}: Noticeably irrelevant content that might be distracting from main request and can be annoying.
       - 0: Largely irrelevant or off-topic and fails to help the user succinctly.

    5. **Cohesiveness ({RubricWeights.COHESIVENESS * 3} to 0):**
       - {RubricWeights.COHESIVENESS * 3}: Logically coherent, well-structured, easy to follow output that is well-organized.
       - {RubricWeights.COHESIVENESS * 2}: Mostly coherent, with minor issues in flow but does not affect the overall understanding.
       - {RubricWeights.COHESIVENESS * 1}: Partially coherent, but somewhat disorganized and can be hard to follow or understand.
       - 0: Disjointed, inconsistent, difficult to follow with no (or minimal) logical structure or coherence.

    6. **Accuracy ({RubricWeights.ACCURACY * 3} to 0)**:
       - {RubricWeights.ACCURACY * 3}: Factually accurate and aligns with instructions, no errors, and provides correct information.
       - {RubricWeights.ACCURACY * 2}: Generally accurate, but may contain minor inaccuracies or slight misinterpretations.
       - {RubricWeights.ACCURACY * 1}: Several inaccuracies, or misunderstandings that might critically affect the quality of the output.
       - 0: Largely inaccurate or misleading, providing incorrect information that is not useful or reliable.

    7. **Naturalness ({RubricWeights.NATURALNESS * 3} to 0)**:
       - {RubricWeights.NATURALNESS * 3}: Sounds natural, representing the correct humanoid tone, and uses human-like words, phrases, and expressions.
       - {RubricWeights.NATURALNESS * 2}: Somewhat natural but occasionally stiff and wooden, sometimes uses boilerplate language.
       - {RubricWeights.NATURALNESS * 1}: Often wooden, overly formal, or awkward phrasing that sounds robotic or unnatural.
       - 0: Very unnatural, very robotic, or overly complicated language that is hard to understand, boring and un-engaging.

    8. **Additional Rubric Parameters:**
        - If provided, additional scoring criteria will be inserted below, along with the maximum and minimum score
        available for them, and formatted as above. If none are provided, ignore this section.

        ```
        {f"{'\n\n'.join(user_defined_criteria)}"}
        ```

        **IMPORTANT NOTES:**

        - If there are additional parameters, THEY MUST NEVER BE CONSIDERED secondary to the main rubric. They should be
        considered equally as important and based on their weight and importance to the user's request, this is exceptionally
        important to remember. For example, if the maximum score of a user defined rubric is higher than an existing rubric
        parameter, it should be considered more important, and vice versa.

    -----

    ## Overall Quality & Interpretation

        - FOR GENERATION ASSISTANT:

        Your goal is to generate high-quality completions that score as high as possible across all given dimensions,
        and don't forget to consider the weight of each dimension.

        - FOR EVALUATION ASSISTANT:

        After scoring each dimension (including any additional parameters if there is any), the total score must be
        calculated by summing up the scores.

        A higher total score indicates better quality, while a lower score indicates a lower quality.

        - FOR IMPROVEMENT ASSISTANT:

        Your goal is to produce improved completions that score as high as possible across all dimensions outlined in the
        **Evaluation Rubric**. Never forget to consider the weight of each dimension.

    -----

    """

    return evaluation_rubric
