#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sinaptera_execution_manager.py
#  Last Modified: 2024-12-14 15:37:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-14 15:37:21
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

import openai
from django.contrib.auth.models import User

from apps.core.generative_ai.utils import (
    ChatRoles,
    GPT_DEFAULT_ENCODING_ENGINE
)

from apps.core.sinaptera.prompts import (
    get_evaluation_system_prompt,
    get_evaluation_user_prompt_template,
    get_improvement_system_prompt,
    get_improvement_user_prompt,
    get_terminal_evaluation_system_prompt,
    get_evaluation_rubric_prompt,
)

from apps.core.sinaptera.utils import (
    SinapteraEvaluationImprovementNitroBoostModels,
    SinapteraCallerTypes
)

from apps.llm_core.models import (
    LLMCore
)
from apps.llm_transaction.models import LLMTransaction

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames,
    LLMTokenTypesNames
)

from apps.multimodal_chat.utils import (
    transmit_websocket_log
)

from apps.sinaptera.models import (
    SinapteraConfiguration
)

logger = logging.getLogger(__name__)


class SinapteraBoosterManager:
    def __init__(
        self,
        user: User,
        llm_core: LLMCore,
        caller_type: str,
    ):

        self.user = user

        sinaptera_configuration, created = SinapteraConfiguration.objects.get_or_create(
            user=user
        )

        sinaptera_configuration: SinapteraConfiguration

        self.sinaptera_configuration = sinaptera_configuration

        if caller_type not in SinapteraCallerTypes.as_list():
            logger.error(f"Invalid caller type: {caller_type}")
            raise ValueError(f"Invalid caller type: {caller_type}")

        self.caller_type = caller_type

        self.llm_core: LLMCore = llm_core

        self.api_key = self.llm_core.api_key
        openai.api_key = self.api_key

        self.generation_model_name = self.llm_core.model_name

        self.nitro_boost = self.sinaptera_configuration.nitro_boost

        if self.nitro_boost is True:
            self.evaluation_model_name = SinapteraEvaluationImprovementNitroBoostModels.NITRO
            self.terminal_evaluation_model_name = SinapteraEvaluationImprovementNitroBoostModels.NITRO
            self.improvement_model_name = SinapteraEvaluationImprovementNitroBoostModels.NITRO

        else:
            self.evaluation_model_name = SinapteraEvaluationImprovementNitroBoostModels.STANDARD
            self.terminal_evaluation_model_name = SinapteraEvaluationImprovementNitroBoostModels.STANDARD
            self.improvement_model_name = SinapteraEvaluationImprovementNitroBoostModels.STANDARD

        self.M = self.sinaptera_configuration.branch_keeping_factor
        self.N = self.sinaptera_configuration.branching_factor
        self.D = self.sinaptera_configuration.evaluation_depth_factor

        evaluation_rubric_prompt = get_evaluation_rubric_prompt(
            sinaptera_configuration=self.sinaptera_configuration
        )

        evaluation_system_prompt = get_evaluation_system_prompt(
            evaluation_rubric_prompt=evaluation_rubric_prompt
        )

        evaluation_user_prompt = get_evaluation_user_prompt_template()

        improvement_system_prompt = get_improvement_system_prompt(
            evaluation_rubric_prompt=evaluation_rubric_prompt
        )

        terminal_evaluation_system_prompt = get_terminal_evaluation_system_prompt(
            evaluation_rubric_prompt=evaluation_rubric_prompt
        )

        self.evaluation_system_prompt = evaluation_system_prompt
        self.evaluation_user_prompt = evaluation_user_prompt

        self.improvement_system_prompt = improvement_system_prompt

        self.terminal_evaluation_system_prompt = terminal_evaluation_system_prompt

    def call_openai_chat(
        self,
        model_name,
        structured_conversation_history: list,
    ):

        context_messages = [
            {
                "role": ChatRoles.SYSTEM,
                "content": structured_conversation_history[0].get("content")
            },
            {
                "role": ChatRoles.USER,
                "content": structured_conversation_history[1].get("content")
            }
        ],

        LLMTransaction.objects.create(
            organization=self.llm_core.organization,
            model=self.llm_core,
            responsible_user=None,
            responsible_assistant=None,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=structured_conversation_history,
            transaction_type=ChatRoles.SYSTEM,
            transaction_source=LLMTransactionSourcesTypesNames.APP,
            llm_token_type=LLMTokenTypesNames.INPUT
        )

        # Evaluation or improvement rounds: Reasoning based generation
        if model_name in SinapteraEvaluationImprovementNitroBoostModels.as_list():
            response = openai.chat.completions.create(
                model=model_name,
                messages=context_messages,
            )

        # Generation rounds: Standard model based generation
        else:
            response = openai.chat.completions.create(
                model=model_name,
                messages=structured_conversation_history,
                # temperature=float(self.llm_core.temperature),
                # frequency_penalty=float(self.llm_core.frequency_penalty),
                # presence_penalty=float(self.llm_core.presence_penalty),
                # max_tokens=int(self.llm_core.maximum_tokens),
                # top_p=float(self.llm_core.top_p),
            )

        final_content = response.choices[0].message.content.strip()

        LLMTransaction.objects.create(
            organization=self.llm_core.organization,
            model=self.llm_core,
            responsible_user=None,
            responsible_assistant=None,
            encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
            transaction_context_content=str(final_content),
            transaction_type=ChatRoles.ASSISTANT,
            transaction_source=LLMTransactionSourcesTypesNames.APP,
            llm_token_type=LLMTokenTypesNames.OUTPUT
        )

        return final_content



    def generate_initial_completions(
        self,
        chat_id: int,
        structured_conversation_history: list
    ) -> list:

        completions = []

        for i in range(self.N):
            logger.info(f"Generating initial completion ({i + 1}/{self.N}).")

            transmit_websocket_log(
                log_message=f"""✴️ Generating initial completion ({i + 1}/{self.N})...""",
                chat_id=chat_id,
                sender_type=self.caller_type
            )

            completion = self.call_openai_chat(
                model_name=self.generation_model_name,
                structured_conversation_history=structured_conversation_history,
            )

            completions.append(completion)

        return completions

    def evaluate_completions_pairwise(
        self,
        chat_id: int,
        user_prompt: str,
        completionA: str,
        completionB: str,
        terminal: bool = False
    ) -> str:

        system_prompt = self.terminal_evaluation_system_prompt if terminal else self.evaluation_system_prompt

        while True:
            logger.info("Evaluation round...")

            transmit_websocket_log(
                log_message=f"""⚖️ Evaluation round is ongoing...""",
                chat_id=chat_id,
                sender_type=self.caller_type
            )

            transmit_websocket_log(
                log_message=f"""🔖 Building evaluation criteria and rubric...""",
                chat_id=chat_id,
                sender_type=self.caller_type
            )

            evaluation_user_prompt_built = self.evaluation_user_prompt.strip() % (
                user_prompt,
                completionA,
                completionB
            )

            transmit_websocket_log(
                log_message=f"""✅ Evaluation criteria and rubric are successfully built.""",
                chat_id=chat_id,
                sender_type=self.caller_type
            )

            structured_evaluation_conversation_history = [
                {
                    "role": ChatRoles.SYSTEM,
                    "content": system_prompt
                },
                {
                    "role": ChatRoles.USER,
                    "content": evaluation_user_prompt_built
                }
            ]

            transmit_websocket_log(
                log_message=f"""🧐 Evaluation agent is interpreting the completions...""",
                chat_id=chat_id,
                sender_type=self.caller_type
            )

            response = self.call_openai_chat(
                model_name=self.terminal_evaluation_model_name if terminal else self.evaluation_model_name,
                structured_conversation_history=structured_evaluation_conversation_history
            )

            transmit_websocket_log(
                log_message=f"""☑️ Evaluation agent has interpreted the completions successfully.""",
                chat_id=chat_id,
                sender_type=self.caller_type
            )

            response = response.strip()

            if response in [
                "A", "B",
                "'A'", "'B'",
                '"A"', '"B"'
            ]:

                transmit_websocket_log(
                    log_message=f"""📦 Evaluation response is extracted successfully.""",
                    chat_id=chat_id,
                    sender_type=self.caller_type
                )

                if (
                    response in ["A", "'A'", '"A"']
                ):
                    return "A"

                if (
                    response in ["B", "'B'", '"B"']
                ):
                    return "B"

            else:

                transmit_websocket_log(
                    log_message=f"""⚠️ Invalid evaluation response received. Agent is trying again to evaluate the completions...""",
                    chat_id=chat_id,
                    sender_type=self.caller_type
                )

                logger.warning("Invalid evaluation response received. Retrying...")

    def prune_completions_to_M(
        self,
        chat_id: int,
        user_prompt: str,
        completions: list,
        terminal: bool = False
    ) -> list:
        current = completions[:]

        iteration_pruning_round = 1
        while len(current) > self.M:

            transmit_websocket_log(
                log_message=f"""✂️ Pruning completions to branch keeping factor M, Iteration [{iteration_pruning_round}]...""",
                chat_id=chat_id,
                sender_type=self.caller_type
            )

            iteration_pruning_round += 1

            next_round = []

            for i in range(0, len(current), 2):

                if i + 1 < len(current):

                    winner = self.evaluate_completions_pairwise(
                        chat_id=chat_id,
                        user_prompt=user_prompt,
                        completionA=current[i],
                        completionB=current[i + 1],
                        terminal=terminal
                    )

                    if winner == "A":
                        next_round.append(current[i])

                    else:
                        next_round.append(current[i + 1])

                else:
                    # Odd number of completions, append the last one without comparison

                    transmit_websocket_log(
                        log_message=f"""🚦 Odd number of completions, appending the last completion without comparison...""",
                        chat_id=chat_id,
                        sender_type=self.caller_type
                    )

                    next_round.append(current[i])

            current = next_round

        transmit_websocket_log(
            log_message=f"""✅ Completions are successfully pruned to branch keeping factor M.""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        return current

    def improve_completions(
        self,
        chat_id: int,
        structured_conversation_history: list,
        completion: str,
    ) -> list:

        transmit_websocket_log(
            log_message=f"""🔖 Building improvement criteria and rubric...""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        improvement_user_prompt_built = get_improvement_user_prompt(
            chat_conversation_history=structured_conversation_history,
            completion_to_improve=completion
        )

        transmit_websocket_log(
            log_message=f"""✅ Improvement criteria and rubric are successfully built.""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        improvements = []

        for i in range(self.N):
            logger.info(f"Improving completion (variation {i + 1}/{self.N})...")

            transmit_websocket_log(
                log_message=f"""🔧 Improving completion with generated [variation {i + 1}/{self.N}]...""",
                chat_id=chat_id,
                sender_type=self.caller_type
            )

            structured_improvement_conversation_history = [
                {
                    "role": ChatRoles.SYSTEM,
                    "content": self.improvement_system_prompt
                },
                {
                    "role": ChatRoles.USER,
                    "content": improvement_user_prompt_built
                }
            ]

            new_completion = self.call_openai_chat(
                model_name=self.improvement_model_name,
                structured_conversation_history=structured_improvement_conversation_history,
            )

            improvements.append(new_completion)

        transmit_websocket_log(
            log_message=f"""☑️ Completion is successfully improved with [{len(improvements)}] variations.""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        return improvements

    def execute(
        self,
        chat_id: int,
        structured_conversation_history: list,
    ) -> str:

        logger.info("Starting the tree search process...")

        transmit_websocket_log(
            log_message=f"""🧠 Sinaptera Tree Booster & Tree of Thoughts Chaining process is starting...""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        transmit_websocket_log(
            log_message=f"""💣 Generating initial completions...""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        completions = self.generate_initial_completions(
            chat_id=chat_id,
            structured_conversation_history=structured_conversation_history
        )

        transmit_websocket_log(
            log_message=f"""✅ Initial completions are successfully generated.""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        transmit_websocket_log(
            log_message=f"""👤 Extracting user message...""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        user_message = structured_conversation_history[-1].get("content")

        transmit_websocket_log(
            log_message=f"""☑️ User message is successfully extracted.""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        transmit_websocket_log(
            log_message=f"""✂️ Pruning initial completions to branch keeping factor M...""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        logger.info("Pruning initial completions to branch keeping factor M...")

        completions = self.prune_completions_to_M(
            chat_id=chat_id,
            user_prompt=user_message,
            completions=completions,
            terminal=False
        )

        transmit_websocket_log(
            log_message=f"""✅ Initial completions are successfully pruned to branch keeping factor M.""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        transmit_websocket_log(
            log_message=f"""🗂 Organizing the branches...""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        current_branches = [completions]

        transmit_websocket_log(
            log_message=f"""☑️ Branches are successfully organized.""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        transmit_websocket_log(
            log_message=f"""🕵 Starting the depth search process...""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        for depth in range(1, self.D + 1):
            logger.info(f"Depth {depth}/{self.D}: Improving and pruning...")

            transmit_websocket_log(
                log_message=f"""🎛 Depth Level [{depth}/{self.D}] is being processed. Improving and pruning...""",
                chat_id=chat_id,
                sender_type=self.caller_type
            )

            new_level_branches = []

            for i, branch_completions in enumerate(current_branches):

                transmit_websocket_log(
                    log_message=f"""🎚 Processing Depth Level [{depth}/{self.D}] and Branch ID [{i + 1}/{len(current_branches)}]. The branch is being processed...""",
                    chat_id=chat_id,
                    sender_type=self.caller_type
                )

                for j, comp in enumerate(branch_completions):
                    transmit_websocket_log(
                        log_message=f"""📝 Processing Depth Level [{depth}/{self.D}], Branch ID [{i + 1}/{len(current_branches)}], and Completion ID [{j + 1}/{len(branch_completions)}]. The completion is being processed...""",
                        chat_id=chat_id,
                        sender_type=self.caller_type
                    )

                    improved = self.improve_completions(
                        chat_id=chat_id,
                        completion=comp,
                        structured_conversation_history=structured_conversation_history
                    )

                    transmit_websocket_log(
                        log_message=f"""☑️ Completion is successfully improved with [{len(improved)}] variations.""",
                        chat_id=chat_id,
                        sender_type=self.caller_type
                    )

                    transmit_websocket_log(
                        log_message=f"""✂️ Pruning Improved Completions at Depth Level [{depth}]: Branch ID: [{i + 1}/{len(current_branches)}]""",
                        chat_id=chat_id,
                        sender_type=self.caller_type
                    )

                    pruned = self.prune_completions_to_M(
                        chat_id=chat_id,
                        user_prompt=user_message,
                        completions=improved,
                        terminal=False
                    )

                    transmit_websocket_log(
                        log_message=f"""☑️ Improved Completions are successfully pruned at Depth Level [{depth}] and Branch ID: [{i + 1}/{len(current_branches)}]""",
                        chat_id=chat_id,
                        sender_type=self.caller_type
                    )

                    new_level_branches.append(pruned)

            current_branches = new_level_branches

        transmit_websocket_log(
            log_message=f"""✅ Depth search process is successfully completed, proceeding to the final evaluation process...""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        transmit_websocket_log(
            log_message=f"""🏁 Starting the final In-Branch evaluation process with a total of [{len(current_branches)}] branches.""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        final_single_completions = []

        for k, branch_completions in enumerate(current_branches):
            transmit_websocket_log(
                log_message=f"""🗳 Processing Final In-Branch Pruning of Completions in Branch: [{k + 1}/{len(current_branches)}]...""",
                chat_id=chat_id,
                sender_type=self.caller_type
            )

            reduced = self.prune_completions_to_M(
                chat_id=chat_id,
                user_prompt=user_message,
                completions=branch_completions,
                terminal=True
            )

            final_single_completions.append(reduced[0])

            transmit_websocket_log(
                log_message=f"""☑️ Final In-Branch Pruning of Completions in Branch is successfully completed for Branch: [{k + 1}/{len(current_branches)}]...""",
                chat_id=chat_id,
                sender_type=self.caller_type
            )

        transmit_websocket_log(
            log_message=f"""✅ Final In-Branch evaluation process is successfully completed, proceeding to the final Inter-Branch evaluation process...""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        transmit_websocket_log(
            log_message=f"""⏱️ Starting the final Inter-Branch evaluation process with a total of [{len(final_single_completions)}] completions.""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        final_list = final_single_completions[:]

        counter_inter_branch_evaluation = 1

        while len(final_list) > 1:
            next_round = []

            transmit_websocket_log(
                log_message=f"""️⏳️ Inter-Branch Evaluation Round [{counter_inter_branch_evaluation}] is ongoing...""",
                chat_id=chat_id,
                sender_type=self.caller_type
            )

            counter_inter_branch_evaluation += 1

            for i in range(0, len(final_list), 2):
                if i + 1 < len(final_list):
                    winner = self.evaluate_completions_pairwise(
                        chat_id=chat_id,
                        user_prompt=user_message,
                        completionA=final_list[i],
                        completionB=final_list[i + 1],
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

        transmit_websocket_log(
            log_message=f"""✅ Final Inter-Branch evaluation process is successfully completed.""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        transmit_websocket_log(
            log_message=f"""🚀 The best completion is successfully selected, search process is completed.""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        transmit_websocket_log(
            log_message=f"""🚀 {best_completion}""",
            chat_id=chat_id,
            sender_type=self.caller_type
        )

        return best_completion
