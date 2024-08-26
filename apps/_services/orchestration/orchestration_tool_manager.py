import json

from apps._services.orchestration.const import get_orchestration_json_decode_error_log, \
    validate_orchestration_main_tool_json, get_no_orchestration_tool_found_error_log
from apps._services.orchestration.runners.worker_tool_runner import run_worker_tool
from apps._services.orchestration.validators.validate_orchestration_assistant_call import \
    validate_orchestration_worker_assistant_call_execution_tool_json
from apps._services.tools.const import ToolTypeNames
from apps.orchestrations.models import Maestro, OrchestrationQuery
from config.settings import MEDIA_URL


class OrchestrationToolManager:

    def __init__(self, maestro: Maestro, query_chat: OrchestrationQuery, tool_usage_json_str: dict):
        self.maestro = maestro
        self.query_chat = query_chat
        self.tool_usage_json_str = tool_usage_json_str
        self.tool_usage_json = {}

    def use_tool(self):
        print("[OrchestrationToolManager.use_tool] Orchestrator is using a tool.")
        try:
            if isinstance(self.tool_usage_json_str, dict):
                self.tool_usage_json = self.tool_usage_json_str
            else:
                self.tool_usage_json = json.loads(self.tool_usage_json_str)
        except Exception as e:
            print("[OrchestrationToolManager.use_tool] Error while loading the Tool Usage JSON: ", e)
            return get_orchestration_json_decode_error_log(error_logs=str(e)), None, None, None, None

        # For file and image generation by the tools
        file_uris, image_uris = [], []

        error = validate_orchestration_main_tool_json(tool_usage_json=self.tool_usage_json)
        print("[OrchestrationToolManager.use_tool] Validation Error: ", error)
        if error: return error, None, None, None, None

        tool_name = self.tool_usage_json.get("tool")
        tool_response = f"""
            Tool Response: {tool_name}

            '''
        """
        assistant_id = self.tool_usage_json.get("parameters").get("assistant_id")
        tool_response += f"""
            Assistant ID: {assistant_id}
        """
        ##################################################
        # Audio Processing Tool
        if tool_name == ToolTypeNames.ORCHESTRATION_WORKER_ASSISTANT_CALL:
            print("[OrchestrationToolManager.use_tool] Orchestrator is using the Worker Assistant Call Tool.")
            error = validate_orchestration_worker_assistant_call_execution_tool_json(
                tool_usage_json=self.tool_usage_json
            )
            if error: return error, None, None, None, None
            worker_assistant_id = self.tool_usage_json.get("parameters").get("assistant_id")
            query_text = self.tool_usage_json.get("parameters").get("query")
            file_urls = self.tool_usage_json.get("parameters").get("file_urls")
            image_urls = self.tool_usage_json.get("parameters").get("image_urls")
            print("[OrchestrationToolManager.use_tool] Worker Assistant ID: ", worker_assistant_id)
            print("[OrchestrationToolManager.use_tool] Query Text: ", query_text)
            worker_assistant_response = run_worker_tool(
                maestro_id=self.maestro.id,
                query_id=self.query_chat.id,
                worker_assistant_id=worker_assistant_id,
                query_text=query_text,
                file_urls=file_urls,
                image_urls=image_urls
            )
            worker_assistant_response_raw_str = json.dumps(worker_assistant_response, sort_keys=True, default=str)
            tool_response += worker_assistant_response_raw_str
        ##################################################
        # ...
        ##################################################
        # IF NO TOOL IS FOUND WITH THE GIVEN NAME
        else:
            print("[OrchestrationToolManager.use_tool] No Orchestration Tool Found with the given name.")
            return get_no_orchestration_tool_found_error_log(query_name=tool_name), tool_name, assistant_id, file_uris, image_uris
        ##################################################
        tool_response += f"""
            '''
        """
        print("-"*50)
        print("[ACTIVE-LOG] [OrchestrationToolManager.use_tool] Tool Response: ", tool_response)
        print("-"*50)
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
        print("[ToolExecutor.use_tool] Tool Response has been returned.")
        return tool_response, tool_name, assistant_id, file_uris, image_uris
