import openai


test_user_criteria_name = "Goofiness"
test_user_criteria_weight = 10000000  # An integer between 0 and 10
test_user_criteria_description_good = "Every word first letter is replaced with the letter 'g' and last letter is replaced with the letter 'y'. without any exceptions."
test_user_criteria_description_okay = "Most words first letter is replaced with the letter 'g' and last letter is replaced with the letter 'y', but there are some exceptions."
test_user_criteria_description_insufficient = "Some words first letter is replaced with the letter 'g' and last letter is replaced with the letter 'y', but there are many exceptions."
test_user_criteria_description_bad = "No words first letter is replaced with the letter 'g' and last letter is replaced with the letter 'y'."

USER_RUBRIC_CRITERION_TEMPLATE = f"""
    --- User Defined Evaluation Criteria ---
    **{test_user_criteria_name} ({test_user_criteria_weight * 3} to 0):**
       - {test_user_criteria_weight * 3}: {test_user_criteria_description_good}
       - {test_user_criteria_weight * 2}: {test_user_criteria_description_okay}
       - {test_user_criteria_weight * 1}: {test_user_criteria_description_insufficient}
       - 0: {test_user_criteria_description_bad}
    --- User Defined Evaluation Criteria ---
"""

USER_DEFINED_CRITERIA = [
    USER_RUBRIC_CRITERION_TEMPLATE
]


EVALUATION_RUBRIC = f"""

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
    {f"{'\n\n'.join(USER_DEFINED_CRITERIA)}"}
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

GENERATION_SYSTEM_PROMPT = f"""

# GENERATION ASSISTANT

You are a helpful assistant that generates high-quality completions.

You will be provided a user prompt and your goal is to generate a completion that is as helpful and informative as possible.
Your answer will be evaluated based on the quality of the response, including a rubric for evaluation.

- Use the **Evaluation Rubric** below to generate a completion that scores as high as possible across all given dimensions,
and don't forget to consider the weight of each dimension.

- Assign each dimension a score between the defined ranges in the metric, according to the descriptions
in the rubric.

```
{EVALUATION_RUBRIC}
```

"""

EVALUATION_SYSTEM_PROMPT = f"""
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
    {EVALUATION_RUBRIC}
    ```

    -----
"""

EVALUATION_USER_PROMPT = """
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

IMPROVEMENT_SYSTEM_PROMPT = f"""

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
    {EVALUATION_RUBRIC}
    ```

    -----
"""

IMPROVEMENT_USER_PROMPT = """

    ### **USER PROMPT:**

    ```
    %s
    ```

    -----

    ### **ORIGINAL COMPLETION (COMPLETION TO IMPROVE):**

    ```
    %s
    ```

    Improve the completion to make it fit better to the user prompt and achieve higher scores across all dimensions
    based on the rubric that is shared with you.

    - You must aim for the highest possible quality score in your improved completion based on the rubric.

    -----
"""

TERMINAL_EVALUATION_SYSTEM_PROMPT = f"""
-----

    # EVALUATION ASSISTANT

    You are an LLM completion evaluation assistant.

    You will be provided the user's prompt and two completions (A and B).

    - Use the **Evaluation Rubric** below to score each completion independently across all given dimensions.
    Never forget to consider the weight of each dimension.

    - Assign each dimension a score between the defined ranges in the metric, according to the descriptions
    in the rubric. Although the rubric provides descriptions for 4 levels of quality, you can use any integer score
    within the range for more granularity by taking the steps as reference points.

    After assigning scores for all dimensions, sum them up to get the total quality score for Completion A and Completion B.

    Compare the totals:

    - If Completion A's total score is higher, choose 'A'.
    - If Completion B's total score is higher, choose 'B'.

    - If there's a tie, break the tie by comparing with your intuitive sense of which completion is better overall.

    Answer strictly with 'A' or 'B' only. No other text or symbols should be included. Do not use quotes as well,
    simply output the letter.

    # EVALUATION RUBRIC

    ```
    {EVALUATION_RUBRIC}
    ```

    -----
"""


class SinapteraBoosterManager:
    def __init__(
        self,
        api_key: str,
        model_name: str = "o3-mini",
        M: int = 2,
        N: int = 4,
        D: int = 2,
        generation_system_prompt=GENERATION_SYSTEM_PROMPT,
        evaluation_system_prompt=EVALUATION_SYSTEM_PROMPT,
        improvement_system_prompt=IMPROVEMENT_SYSTEM_PROMPT,
        terminal_evaluation_system_prompt=TERMINAL_EVALUATION_SYSTEM_PROMPT,
    ):
        self.api_key = api_key
        openai.api_key = api_key
        self.model_name = model_name
        self.M = M
        self.N = N
        self.D = D

        self.generation_system_prompt = generation_system_prompt

        print(generation_system_prompt)

        self.evaluation_system_prompt = evaluation_system_prompt
        self.evaluation_user_prompt = EVALUATION_USER_PROMPT

        self.improvement_system_prompt = improvement_system_prompt
        self.improvement_user_prompt = IMPROVEMENT_USER_PROMPT

        self.terminal_evaluation_system_prompt = terminal_evaluation_system_prompt

    def call_openai_chat(
        self,
        system_prompt,
        user_prompt,
    ):

        response = openai.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "assistant",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
        )

        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

    def generate_initial_completions(
        self, user_prompt: str
    ) -> list:

        completions = []

        for i in range(self.N):
            print(f"Generating initial completion ({i + 1}/{self.N}).")

            completion = self.call_openai_chat(
                system_prompt=self.generation_system_prompt,
                user_prompt=user_prompt,
            )

            completions.append(completion)

        return completions

    def evaluate_completions_pairwise(
        self,
        user_prompt: str,
        completionA: str,
        completionB: str,
        terminal: bool = False
    ) -> str:

        system_prompt = self.terminal_evaluation_system_prompt if terminal else self.evaluation_system_prompt

        while True:
            print("Evaluation round...")

            evaluation_user_prompt_built = self.evaluation_user_prompt.strip() % (
                user_prompt,
                completionA,
                completionB
            )

            response = self.call_openai_chat(
                system_prompt=system_prompt,
                user_prompt=evaluation_user_prompt_built,
            )

            response = response.strip()

            if response in [
                "A", "B",
                "'A'", "'B'",
                '"A"', '"B"'
            ]:

                if response in ["A", "'A'", '"A"']:
                    return "A"

                if response in ["B", "'B'", '"B"']:
                    return "B"

            else:
                print("Invalid evaluation response received. Retrying...")

    def prune_completions_to_M(
        self,
        user_prompt: str,
        completions: list,
        terminal: bool = False
    ) -> list:
        current = completions[:]

        while len(current) > self.M:

            next_round = []

            for i in range(0, len(current), 2):

                if i + 1 < len(current):

                    winner = self.evaluate_completions_pairwise(
                        user_prompt,
                        current[i],
                        current[i + 1],
                        terminal=terminal
                    )

                    if winner == "A":
                        next_round.append(current[i])

                    else:
                        next_round.append(current[i + 1])

                else:
                    # Odd number of completions, append the last one without comparison
                    next_round.append(current[i])

            current = next_round

        return current

    def improve_completions(
        self,
        user_prompt: str,
        completion: str
    ) -> list:

        improvement_user_prompt_built = self.improvement_user_prompt.strip() % (
            user_prompt,
            completion
        )

        improvements = []

        for i in range(self.N):
            print(f"Improving completion (variation {i + 1}/{self.N})...")

            new_completion = self.call_openai_chat(
                system_prompt=self.improvement_system_prompt,
                user_prompt=improvement_user_prompt_built,
            )

            improvements.append(new_completion)

        return improvements

    def build_tree(
        self,
        user_prompt: str
    ) -> str:

        print("Starting the tree search process...")

        completions = self.generate_initial_completions(user_prompt)

        print("Pruning initial completions to M...")

        completions = self.prune_completions_to_M(
            user_prompt,
            completions,
            terminal=False
        )

        current_branches = [completions]

        for depth in range(1, self.D + 1):
            print(f"Depth {depth}/{self.D}: Improving and pruning...")

            new_level_branches = []

            for branch_completions in current_branches:

                for comp in branch_completions:
                    improved = self.improve_completions(
                        user_prompt=user_prompt,
                        completion=comp
                    )

                    pruned = self.prune_completions_to_M(
                        user_prompt=user_prompt,
                        completions=improved,
                        terminal=False
                    )

                    new_level_branches.append(pruned)

            current_branches = new_level_branches

        final_single_completions = []

        for branch_completions in current_branches:
            reduced = self.prune_completions_to_M(
                user_prompt=user_prompt,
                completions=branch_completions,
                terminal=True
            )

            final_single_completions.append(reduced[0])

        final_list = final_single_completions[:]

        while len(final_list) > 1:
            next_round = []

            for i in range(0, len(final_list), 2):
                if i + 1 < len(final_list):
                    winner = self.evaluate_completions_pairwise(
                        user_prompt,
                        final_list[i],
                        final_list[i + 1],
                        terminal=True
                    )

                    if winner == "A":
                        next_round.append(final_list[i])
                    else:
                        next_round.append(final_list[i + 1])
                else:
                    next_round.append(final_list[i])

            final_list = next_round

        best_completion = final_list[0]

        return best_completion


if __name__ == "__main__":
    api_key = "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"

    # Small Test:
    engine = SinapteraBoosterManager(
        api_key=api_key,
        model_name="o3-mini",
        M=1,
        N=2,
        D=1
    )

    user_prompt = "Explain the cat history"

    final_answer = engine.build_tree(user_prompt)

    print("FINAL BEST COMPLETION:\n", final_answer)
