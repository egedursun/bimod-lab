#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: function_utils.py
#  Last Modified: 2024-09-28 20:38:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:05:55
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

#
import tiktoken
import wonderwords
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.llm_transaction.utils import LLMCostsPerMillionTokens, SERVICE_PROFIT_MARGIN, VAT_TAX_RATE
from apps.multimodal_chat.utils import BIMOD_STREAMING_END_TAG, BIMOD_PROCESS_END, BIMOD_NO_TAG_PLACEHOLDER

import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")


def send_log_message(log_message, chat_id, stop_tag=BIMOD_STREAMING_END_TAG):
    channel_layer = get_channel_layer()
    group_name = f'logs_{chat_id}'

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_log',
            'message': log_message,
        }
    )
    if stop_tag == BIMOD_STREAMING_END_TAG:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_log',
                'message': BIMOD_STREAMING_END_TAG,
            }
        )
    elif stop_tag == BIMOD_PROCESS_END:
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_log',
                'message': BIMOD_PROCESS_END,
            }
        )
    else:
        if stop_tag is None or stop_tag == "" or stop_tag == BIMOD_NO_TAG_PLACEHOLDER:
            pass
        else:
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'send_log',
                    'message': stop_tag,
                }
            )


def calculate_number_of_tokens(encoding_engine, text):
    # Tokenize the text
    encoding = tiktoken.get_encoding(encoding_engine)
    tokens = encoding.encode(str(text))
    return len(tokens)


def calculate_llm_cost(model, number_of_tokens):
    costs = LLMCostsPerMillionTokens.OPENAI_GPT_COSTS[model]
    tokens_divided_by_million = number_of_tokens / 1_000_000
    apx_input_cost = (tokens_divided_by_million / 2) * costs["input"]
    apx_output_cost = (tokens_divided_by_million / 2) * costs["output"]
    llm_cost = (apx_input_cost + apx_output_cost)
    return llm_cost


def calculate_internal_service_cost(llm_cost):
    return llm_cost * SERVICE_PROFIT_MARGIN


def calculate_tax_cost(internal_service_cost):
    tax_cost = internal_service_cost * VAT_TAX_RATE
    return tax_cost


def calculate_billable_cost(internal_service_cost, tax_cost):
    return internal_service_cost + tax_cost


def calculate_billable_cost_from_raw(encoding_engine, model, text):
    number_of_tokens = calculate_number_of_tokens(encoding_engine, text)
    llm_cost = calculate_llm_cost(model, number_of_tokens)
    internal_service_cost = calculate_internal_service_cost(llm_cost)
    tax_cost = calculate_tax_cost(internal_service_cost)
    return calculate_billable_cost(internal_service_cost, tax_cost)


def generate_chat_name():
    # use a library to generate a random chat name
    chat_name_1 = wonderwords.RandomWord().word(word_max_length=8, include_categories=["verb"])
    chat_name_2 = wonderwords.RandomWord().word(word_max_length=8, include_categories=["adjective"])
    chat_name_3 = wonderwords.RandomWord().word(word_max_length=8, include_categories=["noun"])
    chat_name_1 = chat_name_1.capitalize()
    chat_name_2 = chat_name_2.capitalize()
    chat_name_3 = chat_name_3.capitalize()
    return " ".join([chat_name_1, chat_name_2, chat_name_3])
