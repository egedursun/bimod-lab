import json

from apps._services.browsers.browser_executor import BrowserActionsNames
from apps._services.llms.helpers.helper_prompts import get_json_decode_error_log
from apps._services.tools.const import ToolTypeNames, get_no_knowledge_base_connection_error_log, \
    get_no_tool_found_error_log
from apps._services.tools.execution_handlers.browser_execution_tool_handler import execute_browser_action
from apps._services.tools.execution_handlers.code_interpreter_execution_handler import execute_code_interpreter
from apps._services.tools.execution_handlers.custom_api_execution_handler import execute_api_executor
from apps._services.tools.execution_handlers.custom_function_execution_handler import execute_custom_code_executor
from apps._services.tools.execution_handlers.custom_script_content_retrieval_handler import retrieve_script_content
from apps._services.tools.execution_handlers.file_system_command_execution_handler import execute_file_system_commands
from apps._services.tools.execution_handlers.image_generator_execution_handler import execute_image_generation
from apps._services.tools.execution_handlers.image_modification_execution_handler import execute_image_modification
from apps._services.tools.execution_handlers.image_variation_execution_handler import execute_image_variation
from apps._services.tools.execution_handlers.knowledge_base_query_execution_handler import execute_knowledge_base_query
from apps._services.tools.execution_handlers.memory_query_execution_handler import execute_memory_query
from apps._services.tools.execution_handlers.nosql_query_execution_handler import execute_nosql_query
from apps._services.tools.execution_handlers.predict_with_ml_model_execution_handler import execute_predict_ml_model
from apps._services.tools.execution_handlers.sql_query_execution_handler import execute_sql_query
from apps._services.tools.execution_handlers.url_file_downloader_execution_handler import execute_url_file_downloader
from apps._services.tools.validators.browser_execution_tool_validator import validate_browser_execution_tool_json
from apps._services.tools.validators.code_interpreter_execution_tool_validator import \
    validate_code_interpreter_execution_tool_json
from apps._services.tools.validators.context_history_query_execution_tool_validator import \
    validate_context_history_query_execution_tool_json
from apps._services.tools.validators.custom_api_execution_tool_validator import validate_custom_api_execution_tool_json
from apps._services.tools.validators.custom_function_execution_tool_validator import \
    validate_custom_function_execution_tool_json
from apps._services.tools.validators.custom_script_content_retriever_tool_validator import \
    validate_custom_script_retriever_tool_json
from apps._services.tools.validators.file_system_command_execution_tool_validator import \
    validate_file_system_command_execution_tool_json
from apps._services.tools.validators.image_generation_tool_validator import validate_image_generation_tool_json
from apps._services.tools.validators.image_modification_tool_validator import validate_image_modification_tool_json
from apps._services.tools.validators.image_variation_tool_validator import validate_image_variation_tool_json
from apps._services.tools.validators.knowledge_base_query_execution_tool_validator import \
    validate_knowledge_base_query_execution_tool_json
from apps._services.tools.validators.main_json_validator import validate_main_tool_json
from apps._services.tools.validators.nosql_query_execution_tool_validator import \
    validate_nosql_query_execution_tool_json
from apps._services.tools.validators.predict_with_ml_model_execution_tool_validator import \
    validate_predict_with_ml_model_execution_tool_json
from apps._services.tools.validators.sql_query_execution_tool_validator import validate_sql_query_execution_tool_json
from apps._services.tools.validators.storage_query_execution_tool_validator import \
    validate_media_storage_query_execution_tool_json
from apps._services.tools.validators.url_file_downloader_execution_tool_validator import \
    validate_url_file_downloader_execution_tool_json
from apps.assistants.models import Assistant
from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
from apps.mm_functions.models import CustomFunction
from apps.multimodal_chat.models import MultimodalChat
from config.settings import MEDIA_URL


class ExecutionTypesNames:
    FILE_INTERPRETATION = "file_interpretation"
    IMAGE_INTERPRETATION = "image_interpretation"


class ToolExecutor:

    def __init__(self, assistant: Assistant, chat: MultimodalChat, tool_usage_json_str: dict):
        self.assistant = assistant
        self.chat = chat
        self.tool_usage_json_str = tool_usage_json_str
        self.tool_usage_json = {}

    def use_tool(self):
        from apps._services.tools.execution_handlers.storage_query_execution_handler import execute_storage_query
        print("[ToolExecutor.use_tool] Tool Usage JSON is being decoded...")
        try:
            if isinstance(self.tool_usage_json_str, dict):
                self.tool_usage_json = self.tool_usage_json_str
            else:
                self.tool_usage_json = json.loads(self.tool_usage_json_str)
        except Exception as e:
            print("[ToolExecutor.use_tool] Error decoding the JSON: ", e)
            return get_json_decode_error_log(error_logs=str(e)), None, None, None

        # For file and image generation by the tools
        file_uris, image_uris = [], []

        error = validate_main_tool_json(tool_usage_json=self.tool_usage_json)
        print("[ToolExecutor.use_tool] Tool Usage JSON has been validated.")
        if error: return error, None, None, None

        tool_name = self.tool_usage_json.get("tool")
        tool_response = f"""
            Tool Response: {tool_name}

            '''
        """

        ##################################################
        # SQL Query Execution Tool
        if tool_name == ToolTypeNames.SQL_QUERY_EXECUTION:
            print("[ToolExecutor.use_tool] SQL Query Execution Tool is being executed...")
            error = validate_sql_query_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            connection_id = self.tool_usage_json.get("parameters").get("database_connection_id")
            query_type = self.tool_usage_json.get("parameters").get("type")
            sql_query = self.tool_usage_json.get("parameters").get("sql_query")
            sql_response = execute_sql_query(connection_id=connection_id, query_type=query_type, sql_query=sql_query)
            sql_response_raw_str = json.dumps(sql_response, sort_keys=True, default=str)
            tool_response += sql_response_raw_str
        ##################################################
        # NoSQL Query Execution Tool
        elif tool_name == ToolTypeNames.NOSQL_QUERY_EXECUTION:
            print("[ToolExecutor.use_tool] NoSQL Query Execution Tool is being executed...")
            error = validate_nosql_query_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            connection_id = self.tool_usage_json.get("parameters").get("database_connection_id")
            query_type = self.tool_usage_json.get("parameters").get("type")
            nosql_query = self.tool_usage_json.get("parameters").get("query")
            nosql_response = execute_nosql_query(connection_id=connection_id, query_type=query_type,
                                                 nosql_query=nosql_query)
            nosql_response_raw_str = json.dumps(nosql_response, sort_keys=True, default=str)
            tool_response += nosql_response_raw_str
        ##################################################
        # Knowledge Base Query Execution Tool
        elif tool_name == ToolTypeNames.KNOWLEDGE_BASE_QUERY_EXECUTION:
            print("[ToolExecutor.use_tool] Knowledge Base Query Execution Tool is being executed...")
            error = validate_knowledge_base_query_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            connection_id = self.tool_usage_json.get("parameters").get("knowledge_base_connection_id")
            query = self.tool_usage_json.get("parameters").get("query")
            alpha = self.tool_usage_json.get("parameters").get("alpha")
            knowledge_base_response = execute_knowledge_base_query(connection_id=connection_id, query=query,
                                                                   alpha=alpha)
            knowledge_base_response_raw_str = json.dumps(knowledge_base_response, sort_keys=True, default=str)
            tool_response += knowledge_base_response_raw_str
        ##################################################
        # Vector Chat History Query Execution Tool
        elif tool_name == ToolTypeNames.VECTOR_CHAT_HISTORY_QUERY_EXECUTION:
            print("[ToolExecutor.use_tool] Vector Chat History Query Execution Tool is being executed...")
            error = validate_context_history_query_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            connection = ContextHistoryKnowledgeBaseConnection.objects.filter(chat=self.chat,
                                                                              assistant=self.assistant).first()
            if not connection:
                return get_no_knowledge_base_connection_error_log(assistant_name=self.assistant.name,
                                                                  chat_name=self.chat.chat_name), None, None, None
            query = self.tool_usage_json.get("parameters").get("query")
            alpha = self.tool_usage_json.get("parameters").get("alpha")
            knowledge_base_response = execute_memory_query(
                connection_id=connection.id,
                query=query,
                alpha=alpha
            )
            knowledge_base_response_raw_str = json.dumps(knowledge_base_response, sort_keys=True, default=str)
            tool_response += knowledge_base_response_raw_str
        ##################################################
        # File System Command Execution Tool
        elif tool_name == ToolTypeNames.FILE_SYSTEM_COMMAND_EXECUTION:
            print("[ToolExecutor.use_tool] File System Command Execution Tool is being executed...")
            error = validate_file_system_command_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            connection_id = self.tool_usage_json.get("parameters").get("file_system_connection_id")
            commands = self.tool_usage_json.get("parameters").get("commands")
            file_system_response = execute_file_system_commands(connection_id=connection_id, commands=commands)
            file_system_response_raw_str = json.dumps(file_system_response, sort_keys=True, default=str)
            tool_response += file_system_response_raw_str
        ##################################################
        # Media Storage Query Execution Tool
        elif tool_name == ToolTypeNames.MEDIA_STORAGE_QUERY_EXECUTION:
            print("[ToolExecutor.use_tool] Media Storage Query Execution Tool is being executed...")
            error = validate_media_storage_query_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            connection_id = self.tool_usage_json.get("parameters").get("media_storage_connection_id")
            chat_id = self.chat.id
            query = self.tool_usage_json.get("parameters").get("query")
            type = self.tool_usage_json.get("parameters").get("type")
            file_paths = self.tool_usage_json.get("parameters").get("file_paths")
            media_storage_response, file_uris, image_uris = execute_storage_query(
                connection_id=connection_id, chat_id=chat_id, execution_type=type, file_paths=file_paths, query=query)
            response_raw_str = json.dumps(media_storage_response, sort_keys=True, default=str)
            tool_response += response_raw_str
        ##################################################
        # URL File Downloader Tool
        elif tool_name == ToolTypeNames.URL_FILE_DOWNLOADER:
            print("[ToolExecutor.use_tool] URL File Downloader Tool is being executed...")
            error = validate_url_file_downloader_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            connection_id = self.tool_usage_json.get("parameters").get("media_storage_connection_id")
            download_url = self.tool_usage_json.get("parameters").get("url")
            url_downloader_response = execute_url_file_downloader(connection_id=connection_id, url=download_url)
            url_downloader_response_raw_str = json.dumps(url_downloader_response, sort_keys=True, default=str)
            tool_response += url_downloader_response_raw_str
        ##################################################
        # Prediction with ML Model Tool
        elif tool_name == ToolTypeNames.PREDICTION_WITH_ML_MODEL:
            print("[ToolExecutor.use_tool] Prediction with ML Model Tool is being executed...")
            error = validate_predict_with_ml_model_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            ml_base_connection_id = self.tool_usage_json.get("parameters").get("ml_base_connection_id")
            model_path = self.tool_usage_json.get("parameters").get("model_path")
            input_data_paths = self.tool_usage_json.get("parameters").get("input_data_paths")
            query = self.tool_usage_json.get("parameters").get("query")
            predict_ml_response = execute_predict_ml_model(connection_id=ml_base_connection_id, chat_id=self.chat.id,
                                                           model_url=model_path, input_data_paths=input_data_paths,
                                                           query=query)
            predict_ml_response_raw_str = json.dumps(predict_ml_response, sort_keys=True, default=str)
            tool_response += predict_ml_response_raw_str
        ##################################################
        # Code Interpretation Tool
        elif tool_name == ToolTypeNames.CODE_INTERPRETER:
            print("[ToolExecutor.use_tool] Code Interpreter Tool is being executed...")
            error = validate_code_interpreter_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            file_paths = self.tool_usage_json.get("parameters").get("file_paths")
            query_string = self.tool_usage_json.get("parameters").get("query")
            execute_code_response, file_uris, image_uris = execute_code_interpreter(assistant_id=self.assistant.id, chat_id=self.chat.id,
                                                             file_paths=file_paths, query=query_string)
            code_interpreter_response_raw_str = json.dumps(execute_code_response, sort_keys=True, default=str)
            tool_response += code_interpreter_response_raw_str
        ##################################################
        # Custom Function Executor Tool
        elif tool_name == ToolTypeNames.CUSTOM_FUNCTION_EXECUTOR:
            print("[ToolExecutor.use_tool] Custom Function Executor Tool is being executed...")
            error = validate_custom_function_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            custom_function_reference_id = self.tool_usage_json.get("parameters").get("custom_function_reference_id")
            input_data = self.tool_usage_json.get("parameters").get("input_data")
            custom_function_response = execute_custom_code_executor(
                custom_function_reference_id=custom_function_reference_id,
                input_values=input_data)
            custom_function_response_raw_str = json.dumps(custom_function_response, sort_keys=True, default=str)
            tool_response += custom_function_response_raw_str
        ##################################################
        # Custom API Executor Tool
        elif tool_name == ToolTypeNames.CUSTOM_API_EXECUTOR:
            print("[ToolExecutor.use_tool] Custom API Executor Tool is being executed...")
            error = validate_custom_api_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            custom_api_reference_id = self.tool_usage_json.get("parameters").get("custom_api_reference_id")
            endpoint_name = self.tool_usage_json.get("parameters").get("endpoint_name")
            path_values = self.tool_usage_json.get("parameters").get("path_values")
            query_values = self.tool_usage_json.get("parameters").get("query_values")
            body_values = self.tool_usage_json.get("parameters").get("body_values")
            custom_api_response = execute_api_executor(custom_api_reference_id=custom_api_reference_id,
                                                       endpoint_name=endpoint_name, path_values=path_values,
                                                       query_values=query_values, body_values=body_values)
            custom_api_response_raw_str = json.dumps(custom_api_response, sort_keys=True, default=str)
            tool_response += custom_api_response_raw_str
        ##################################################
        # Custom Script Content Retrieval Tool
        elif tool_name == ToolTypeNames.CUSTOM_SCRIPT_CONTENT_RETRIEVAL:
            print("[ToolExecutor.use_tool] Custom Script Content Retrieval Tool is being executed...")
            error = validate_custom_script_retriever_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            custom_script_reference_id = self.tool_usage_json.get("parameters").get("custom_script_reference_id")
            custom_script_content_response = retrieve_script_content(
                custom_script_reference_id=custom_script_reference_id)
            custom_script_content_response_raw_str = json.dumps(custom_script_content_response, sort_keys=True,
                                                                default=str)
            tool_response += custom_script_content_response_raw_str
        ##################################################
        # Image Generation Tool
        elif tool_name == ToolTypeNames.IMAGE_GENERATION:
            print("[ToolExecutor.use_tool] Image Generation Tool is being executed...")
            error = validate_image_generation_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            prompt = self.tool_usage_json.get("parameters").get("prompt")
            size = self.tool_usage_json.get("parameters").get("size")
            quality = self.tool_usage_json.get("parameters").get("quality")
            image_generation_response = execute_image_generation(assistant_id=self.assistant.id, chat_id=self.chat.id,
                                                                 prompt=prompt + f"""
                                                                    **Important Note:**
                                                                    Always include the generated image's URL in your
                                                                    response's image_uris list or the equivalent.
                                                                 """, image_size=size, quality=quality)
            image_uri = image_generation_response.get("image_uri")
            image_uris.append(image_uri)
            image_generation_response_raw_str = json.dumps(image_generation_response, sort_keys=True, default=str)
            tool_response += image_generation_response_raw_str
        ##################################################
        # Image Modification Tool
        elif tool_name == ToolTypeNames.IMAGE_MODIFICATION:
            print("[ToolExecutor.use_tool] Image Modification Tool is being executed...")
            error = validate_image_modification_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            prompt = self.tool_usage_json.get("parameters").get("prompt")
            edit_image_uri = self.tool_usage_json.get("parameters").get("edit_image_uri")
            edit_image_mask_uri = self.tool_usage_json.get("parameters").get("edit_image_mask_uri")
            image_size = self.tool_usage_json.get("parameters").get("image_size")
            image_modification_response = execute_image_modification(assistant_id=self.assistant.id,
                                                                     chat_id=self.chat.id,
                                                                     prompt=prompt, edit_image_uri=edit_image_uri,
                                                                     edit_image_mask_uri=edit_image_mask_uri,
                                                                     image_size=image_size)
            image_uri = image_modification_response.get("image_uri")
            image_uris.append(image_uri)
            image_modification_response_raw_str = json.dumps(image_modification_response, sort_keys=True, default=str)
            tool_response += image_modification_response_raw_str
        ##################################################
        # Image Variation Creation Tool
        elif tool_name == ToolTypeNames.IMAGE_VARIATION:
            print("[ToolExecutor.use_tool] Image Variation Tool is being executed...")
            error = validate_image_variation_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            image_uri = self.tool_usage_json.get("parameters").get("image_uri")
            image_size = self.tool_usage_json.get("parameters").get("image_size")
            image_variation_response = execute_image_variation(assistant_id=self.assistant.id, chat_id=self.chat.id,
                                                               image_uri=image_uri, image_size=image_size)
            image_uri = image_variation_response.get("image_uri")
            image_uris.append(image_uri)
            image_variation_response_raw_str = json.dumps(image_variation_response, sort_keys=True, default=str)
            tool_response += image_variation_response_raw_str
        ##################################################
        # Browsing Tool
        elif tool_name == ToolTypeNames.BROWSING:
            print("[ToolExecutor.use_tool] Browsing Tool is being executed...")
            error = validate_browser_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None, None, None
            connection_id = self.tool_usage_json.get("parameters").get("browser_connection_id")
            action = self.tool_usage_json.get("parameters").get("action")
            query, page, search_results, click_url = None, None, None, None
            if action == BrowserActionsNames.BROWSER_SEARCH:
                query = self.tool_usage_json.get("parameters").get("query")
                page = self.tool_usage_json.get("parameters").get("page")
            elif action == BrowserActionsNames.CLICK_URL_IN_SEARCH:
                search_results = self.tool_usage_json.get("parameters").get("search_results")
                click_url = self.tool_usage_json.get("parameters").get("click_url")
            browser_response = execute_browser_action(connection_id=connection_id, action=action, query=query,
                                                      page=page, search_results=search_results, click_url=click_url)
            browser_response_raw_str = json.dumps(browser_response, sort_keys=True, default=str)
            tool_response += browser_response_raw_str
        ##################################################
        # ...
        ##################################################
        # IF NO TOOL IS FOUND WITH THE GIVEN NAME
        else:
            print("[ToolExecutor.use_tool] No Tool Found with the given name.")
            return get_no_tool_found_error_log(query_name=tool_name), tool_name, file_uris, image_uris
        ##################################################
        tool_response += f"""
            '''
        """
        print("-"*50)
        print("[ACTIVE-LOG] [ToolExecutor.use_tool] Tool Response Debugger: \n", tool_response)
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
        return tool_response, tool_name, file_uris, image_uris
