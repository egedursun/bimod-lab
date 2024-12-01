#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: harmoniq_tool_manager.py
#  Last Modified: 2024-10-11 21:22:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-11 21:22:57
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

from apps.core.generative_ai.auxiliary_methods.errors.error_log_prompts import get_json_decode_error_log

from apps.core.tool_calls.harmoniq.core_services.core_service_query_expert_network_harmoniq import (
    execute_expert_network_query_harmoniq
)

from apps.core.tool_calls.harmoniq.input_verifiers.verify_expert_network_query_harmoniq import (
    verify_expert_network_query_content_harmoniq
)

from apps.core.tool_calls.input_verifiers.verify_main_query_or_run_call import verify_main_call_or_query_content

from apps.core.tool_calls.utils import (
    ToolCallDescriptorNames,
    get_no_tool_found_error_log
)

from apps.harmoniq.models import Harmoniq
from config.settings import MEDIA_URL

logger = logging.getLogger(__name__)


class HarmoniqToolManager:

    def __init__(
        self,
        agent: Harmoniq,
        tool_usage_json_str: dict
    ):
        self.agent = agent
        self.tool_usage_dict_stringified = tool_usage_json_str
        self.tool_usage_dict = {}

    def call_internal_tool_service_harmoniq(self):

        try:

            if isinstance(self.tool_usage_dict_stringified, dict):
                self.tool_usage_dict = self.tool_usage_dict_stringified
                logger.info("Tool usage dictionary is already a dictionary.")

            else:
                self.tool_usage_dict = json.loads(self.tool_usage_dict_stringified)
                logger.info("Tool usage dictionary is converted to a dictionary.")

        except Exception as e:

            logger.error(f"Error occurred while converting tool usage dictionary to a dictionary: {e}")
            return get_json_decode_error_log(error_logs=str(e)), None, None, None

        f_uris, img_uris = [], []
        error_msg = verify_main_call_or_query_content(
            content=self.tool_usage_dict
        )

        if error_msg:
            logger.error(f"Error occurred while verifying main call or query content: {error_msg}")
            return error_msg, None, None, None

        defined_tool_descriptor = self.tool_usage_dict.get("tool")
        output_tool_call = f"""
                    Tool Response: {defined_tool_descriptor}

                    '''
                """

        if defined_tool_descriptor == ToolCallDescriptorNames.EXECUTE_EXPERT_NETWORK_QUERY:
            error_msg = verify_expert_network_query_content_harmoniq(content=self.tool_usage_dict)

            if error_msg:
                return error_msg, None, None, None

            assistant_id = self.tool_usage_dict.get("parameters").get("assistant_id")
            query = self.tool_usage_dict.get("parameters").get("query")
            image_urls = self.tool_usage_dict.get("parameters").get("image_urls")
            file_urls = self.tool_usage_dict.get("parameters").get("file_urls")

            expert_network_response = execute_expert_network_query_harmoniq(
                agent_id=assistant_id,
                xn_query=query,
                img_uris=image_urls,
                f_uris=file_urls
            )

            expert_network_response_raw_str = json.dumps(
                expert_network_response,
                sort_keys=True,
                default=str
            )

            output_tool_call += expert_network_response_raw_str
            logger.info("Expert network query executed successfully.")

        # NO TOOL FOUND
        else:
            logger.error(f"No tool found with the descriptor: {defined_tool_descriptor}")

            return (
                get_no_tool_found_error_log(
                    query_name=defined_tool_descriptor
                ),
                defined_tool_descriptor,
                f_uris,
                img_uris
            )

        output_tool_call += f"""
                    '''
                """
        if f_uris:
            for i, uri in enumerate(f_uris):
                if not uri.startswith("http"):
                    uri = f"{MEDIA_URL}{uri}"
                f_uris[i] = uri

        if img_uris:
            for i, uri in enumerate(img_uris):
                if not uri.startswith("http"):
                    uri = f"{MEDIA_URL}{uri}"
                img_uris[i] = uri

        logger.info("Tool call service executed successfully.")
        return output_tool_call, defined_tool_descriptor, f_uris, img_uris
