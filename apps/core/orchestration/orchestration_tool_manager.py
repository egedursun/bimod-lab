#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: orchestration_tool_manager.py
#  Last Modified: 2024-10-05 02:25:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
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

from apps.core.orchestration.utils import get_orchestration_json_decode_error_log, \
    validate_orchestration_main_tool_json, get_no_orchestration_tool_found_error_log
from apps.core.orchestration.runners.worker_tool_runner import run_worker_tool
from apps.core.orchestration.validators.validate_orchestration_assistant_call import \
    validate_orchestration_worker_assistant_call_execution_tool_json
from apps.core.tool_calls.utils import ToolCallDescriptorNames
from apps.orchestrations.models import Maestro, OrchestrationQuery
from config.settings import MEDIA_URL


logger = logging.getLogger(__name__)


class OrchestrationToolManager:

    def __init__(self, maestro: Maestro, query_chat: OrchestrationQuery, tool_usage_json_str: dict):
        self.maestro = maestro
        self.query_chat = query_chat
        self.tool_usage_json_str = tool_usage_json_str
        self.tool_usage_json = {}

    def use_tool(self):
        try:
            if isinstance(self.tool_usage_json_str, dict):
                self.tool_usage_json = self.tool_usage_json_str
            else:
                self.tool_usage_json = json.loads(self.tool_usage_json_str)
            logger.info(f"[OrchestrationToolManager.use_tool] The tool usage JSON is loaded successfully.")
        except Exception as e:
            logger.error(f"[OrchestrationToolManager.use_tool] An error occurred while loading the tool usage JSON:", e)
            return get_orchestration_json_decode_error_log(error_logs=str(e)), None, None, None, None

        file_uris, image_uris = [], []
        error = validate_orchestration_main_tool_json(tool_usage_json=self.tool_usage_json)
        if error: return error, None, None, None, None
        tool_name = self.tool_usage_json.get("tool")
        tool_resp = f"""
            Tool Response: {tool_name}

            '''
        """
        agent_id = self.tool_usage_json.get("parameters").get("assistant_id")
        tool_resp += f"""
            Assistant ID: {agent_id}
        """

        if tool_name == ToolCallDescriptorNames.EXECUTE_ORCHESTRATION_WORKER_CONSULTANCY:
            error = validate_orchestration_worker_assistant_call_execution_tool_json(
                tool_usage_json=self.tool_usage_json)
            if error:
                logger.error(f"[OrchestrationToolManager.use_tool] An error occurred while validating the worker "
                             f"assistant call execution tool JSON: {error}")
                return error, None, None, None, None
            worker_assistant_id = self.tool_usage_json.get("parameters").get("assistant_id")
            query_text = self.tool_usage_json.get("parameters").get("query")
            file_urls = self.tool_usage_json.get("parameters").get("file_urls")
            image_urls = self.tool_usage_json.get("parameters").get("image_urls")
            worker_agent_resp = run_worker_tool(
                maestro_id=self.maestro.id, query_id=self.query_chat.id, worker_assistant_id=worker_assistant_id,
                query_text=query_text, file_urls=file_urls, image_urls=image_urls)
            worker_agent_resp_raw_str = json.dumps(worker_agent_resp, sort_keys=True, default=str)
            tool_resp += worker_agent_resp_raw_str

        # TOOLS: NO TOOL SPECIFIED
        else:
            logger.error(f"[OrchestrationToolManager.use_tool] No orchestration tool found with the name: {tool_name}")
            return get_no_orchestration_tool_found_error_log(
                query_name=tool_name), tool_name, agent_id, file_uris, image_uris
        ##################################################
        tool_resp += f"""
            '''
        """
        if file_uris:
            for i, uri in enumerate(file_uris):
                if not uri.startswith("http"):
                    uri = f"{MEDIA_URL}{uri}"
                file_uris[i] = uri
        if image_uris:
            for i, uri in enumerate(image_uris):
                if not uri.startswith("http"):
                    uri = f"{MEDIA_URL}{uri}"
                image_uris[i] = uri
        logger.info(f"[OrchestrationToolManager.use_tool] The tool response is prepared successfully.")
        return tool_resp, tool_name, agent_id, file_uris, image_uris
