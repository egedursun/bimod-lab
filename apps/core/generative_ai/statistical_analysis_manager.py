#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#

import json

from apps.core.generative_ai.auxiliary_methods.errors.error_log_prompts import get_statistics_analysis_error_log
from apps.core.generative_ai.gpt_openai_manager import OpenAIGPTClientManager
from apps.core.generative_ai.utils import DEFAULT_STATISTICS_ASSISTANT_NAME_PLACEHOLDER, \
    DEFAULT_STATISTICS_ASSISTANT_AUDIENCE, DEFAULT_STATISTICS_ASSISTANT_TONE, DEFAULT_STATISTICS_ASSISTANT_CHAT_NAME, \
    DEFAULT_STATISTICS_TEMPERATURE, DEFAULT_STATISTICS_ANALYSIS_MAX_TOKENS
from apps.core.system_prompts.system_prompt_factory_builder import SystemPromptFactoryBuilder
from apps.core.system_prompts.dashboard_analysis.dashboard_statistics_prompt import build_dashboard_statistics_prompt


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
                {"role": "system", "content": json.dumps(lean_prompt, indent=4, sort_keys=True, default=str)}
            ],
            temperature=DEFAULT_STATISTICS_TEMPERATURE, max_tokens=DEFAULT_STATISTICS_ANALYSIS_MAX_TOKENS)
        choices = output.choices
        first_choice = choices[0]
        choice_message = first_choice.message
        choice_message_content = choice_message.content
        output = choice_message_content
    except Exception as e:
        output = get_statistics_analysis_error_log(error_logs=str(e))
    return output
