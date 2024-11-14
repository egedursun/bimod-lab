#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: statistical_analysis_manager.py
#  Last Modified: 2024-10-09 00:27:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 00:27:18
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import json
import logging

from apps.core.generative_ai.auxiliary_methods.errors.error_log_prompts import get_statistics_analysis_error_log
from apps.core.generative_ai.gpt_openai_manager import OpenAIGPTClientManager
from apps.core.generative_ai.utils import DEFAULT_STATISTICS_ASSISTANT_NAME_PLACEHOLDER, \
    DEFAULT_STATISTICS_ASSISTANT_AUDIENCE, DEFAULT_STATISTICS_ASSISTANT_TONE, DEFAULT_STATISTICS_ASSISTANT_CHAT_NAME, \
    DEFAULT_STATISTICS_TEMPERATURE, DEFAULT_STATISTICS_ANALYSIS_MAX_TOKENS
from apps.core.system_prompts.system_prompt_factory_builder import SystemPromptFactoryBuilder
from apps.core.system_prompts.dashboard_analysis.dashboard_statistics_prompt import build_dashboard_statistics_prompt


logger = logging.getLogger(__name__)


def provide_analysis(llm_model, statistics):
    try:
        instructions = build_dashboard_statistics_prompt(statistics=statistics)
        lean_prompt = SystemPromptFactoryBuilder.build_lean(
            assistant_name=DEFAULT_STATISTICS_ASSISTANT_NAME_PLACEHOLDER, instructions=instructions,
            audience=DEFAULT_STATISTICS_ASSISTANT_AUDIENCE, tone=DEFAULT_STATISTICS_ASSISTANT_TONE,
            chat_name=DEFAULT_STATISTICS_ASSISTANT_CHAT_NAME)

        c = OpenAIGPTClientManager.get_naked_client(llm_model=llm_model)
        output = c.chat.completions.create(
            model=llm_model.model_name,
            messages=[
                {"role": "system", "content": json.dumps(lean_prompt, indent=4, sort_keys=True, default=str)},
                {"role": "system", "content": """
                    ===========================
                    # **VERY IMPORTANT NOTE:**
                    ===========================
                    [1] NEVER ASK QUESTIONS, USER CAN'T ANSWER YOU!
                    [2] ALWAYS SHARE YOUR INSIGHTS BASED ON THE DATA, NEVER GREET THE USER!
                    [3] REPEATING AGAIN: NEVER ASK QUESTIONS, NEVER REJECT GENERATING INSIGHTS AND RECOMMENDATIONS!
                    [4] YOUR '''ONLY TASK''' IS TO PROVIDE INSIGHTS AND RECOMMENDATIONS BASED ON THE DATA, NOTHING ELSE!
                    [5] REPEATING AGAIN: NEVER ASK QUESTIONS, NEVER REJECT GENERATING INSIGHTS AND RECOMMENDATIONS!
                    ===========================
                """}
            ],
            temperature=DEFAULT_STATISTICS_TEMPERATURE, max_tokens=DEFAULT_STATISTICS_ANALYSIS_MAX_TOKENS)
        choices = output.choices
        first_choice = choices[0]
        choice_message = first_choice.message
        choice_message_content = choice_message.content
        output = choice_message_content
        logger.info("Analysis has been provided successfully by the system.")
    except Exception as e:
        logger.error(f"An error occurred while providing analysis: {str(e)}")
        output = get_statistics_analysis_error_log(error_logs=str(e))
    return output
