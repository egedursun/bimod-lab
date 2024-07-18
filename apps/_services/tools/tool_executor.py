import json

from apps._services.tools.const import ToolTypeNames
from apps._services.tools.execution_handlers.file_system_command_execution_handler import execute_file_system_commands
from apps._services.tools.execution_handlers.knowledge_base_query_execution_handler import execute_knowledge_base_query
from apps._services.tools.execution_handlers.memory_query_execution_handler import execute_memory_query
from apps._services.tools.execution_handlers.nosql_query_execution_handler import execute_nosql_query
from apps._services.tools.execution_handlers.sql_query_execution_handler import execute_sql_query
from apps._services.tools.validators.context_history_query_execution_tool_validator import \
    validate_context_history_query_execution_tool_json
from apps._services.tools.validators.file_system_command_execution_tool_validator import \
    validate_file_system_command_execution_tool_json
from apps._services.tools.validators.knowledge_base_query_execution_tool_validator import \
    validate_knowledge_base_query_execution_tool_json
from apps._services.tools.validators.main_json_validator import validate_main_tool_json
from apps._services.tools.validators.nosql_query_execution_tool_validator import \
    validate_nosql_query_execution_tool_json
from apps._services.tools.validators.sql_query_execution_tool_validator import validate_sql_query_execution_tool_json
from apps._services.tools.validators.storage_query_execution_tool_validator import \
    validate_media_storage_query_execution_tool_json
from apps.assistants.models import Assistant
from apps.datasource_knowledge_base.models import ContextHistoryKnowledgeBaseConnection
from apps.multimodal_chat.models import MultimodalChat


class ExecutionTypesNames:
    FILE_INTERPRETATION = "file_interpretation"
    IMAGE_INTERPRETATION = "image_interpretation"


class ToolExecutor:

    def __init__(self, assistant: Assistant, chat: MultimodalChat, tool_usage_json_str: dict):
        self.assistant = assistant
        self.chat = chat
        self.tool_usage_json_str = tool_usage_json_str
        self.tool_usage_json = {}
        try:
            self.tool_usage_json = json.loads(tool_usage_json_str)
        except Exception as e:
            print("Error decoding the JSON: ", e)
            raise Exception("Error decoding the JSON")

    def use_tool(self):
        from apps._services.tools.execution_handlers.storage_query_execution_handler import execute_storage_query

        # For file and image generation by the tools
        file_uris, image_uris = [], []

        error = validate_main_tool_json(tool_usage_json=self.tool_usage_json)
        if error: return error, None

        tool_name = self.tool_usage_json.get("tool")
        tool_response = f"""
            Tool Response: {tool_name}

            '''
        """

        ##################################################
        # SQL Query Execution Tool
        if tool_name == ToolTypeNames.SQL_QUERY_EXECUTION:
            error = validate_sql_query_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None

            connection_id = self.tool_usage_json.get("parameters").get("database_connection_id")
            query_type = self.tool_usage_json.get("parameters").get("type")
            sql_query = self.tool_usage_json.get("parameters").get("sql_query")
            sql_response = execute_sql_query(
                connection_id=connection_id,
                query_type=query_type,
                sql_query=sql_query
            )
            # Convert the tool response to a string and pretty format
            sql_response_raw_str = json.dumps(sql_response, sort_keys=True, default=str)
            tool_response += sql_response_raw_str
        ##################################################
        # NoSQL Query Execution Tool
        elif tool_name == ToolTypeNames.NOSQL_QUERY_EXECUTION:
            error = validate_nosql_query_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None

            connection_id = self.tool_usage_json.get("parameters").get("database_connection_id")
            query_type = self.tool_usage_json.get("parameters").get("type")
            nosql_query = self.tool_usage_json.get("parameters").get("query")
            nosql_response = execute_nosql_query(
                connection_id=connection_id,
                query_type=query_type,
                nosql_query=nosql_query
            )
            # Convert the tool response to a string and pretty format
            nosql_response_raw_str = json.dumps(nosql_response, sort_keys=True, default=str)
            tool_response += nosql_response_raw_str
        ##################################################
        # Knowledge Base Query Execution Tool
        elif tool_name == ToolTypeNames.KNOWLEDGE_BASE_QUERY_EXECUTION:
            error = validate_knowledge_base_query_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None

            connection_id = self.tool_usage_json.get("parameters").get("knowledge_base_connection_id")
            query = self.tool_usage_json.get("parameters").get("query")
            alpha = self.tool_usage_json.get("parameters").get("alpha")
            knowledge_base_response = execute_knowledge_base_query(
                connection_id=connection_id,
                query=query,
                alpha=alpha
            )
            # Convert the tool response to a string and pretty format
            knowledge_base_response_raw_str = json.dumps(knowledge_base_response, sort_keys=True, default=str)
            tool_response += knowledge_base_response_raw_str
        ##################################################
        # Vector Chat History Query Execution Tool
        elif tool_name == ToolTypeNames.VECTOR_CHAT_HISTORY_QUERY_EXECUTION:
            error = validate_context_history_query_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None

            connection = ContextHistoryKnowledgeBaseConnection.objects.filter(
                chat=self.chat,
                assistant=self.assistant
            ).first()

            if not connection:
                return f"""
                    The Context History Knowledge Base Connection for the chat: {self.chat.chat_name} and assistant: {self.assistant.name}
                    does not exist in the system. Please make sure you have the connection setup in the system.
                """, None

            query = self.tool_usage_json.get("parameters").get("query")
            alpha = self.tool_usage_json.get("parameters").get("alpha")

            knowledge_base_response = execute_memory_query(
                connection_id=connection.id,
                query=query,
                alpha=alpha
            )
            # Convert the tool response to a string and pretty format
            knowledge_base_response_raw_str = json.dumps(knowledge_base_response, sort_keys=True, default=str)
            tool_response += knowledge_base_response_raw_str
        ##################################################
        # File System Command Execution Tool
        elif tool_name == ToolTypeNames.FILE_SYSTEM_COMMAND_EXECUTION:
            error = validate_file_system_command_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None

            connection_id = self.tool_usage_json.get("parameters").get("file_system_connection_id")
            commands = self.tool_usage_json.get("parameters").get("commands")
            file_system_response = execute_file_system_commands(
                connection_id=connection_id,
                commands=commands
            )
            # Convert the tool response to a string and pretty format
            file_system_response_raw_str = json.dumps(file_system_response, sort_keys=True, default=str)
            tool_response += file_system_response_raw_str
        ##################################################
        # Media Storage Query Execution Tool
        elif tool_name == ToolTypeNames.MEDIA_STORAGE_QUERY_EXECUTION:
            error = validate_media_storage_query_execution_tool_json(tool_usage_json=self.tool_usage_json)
            if error: return error, None

            connection_id = self.tool_usage_json.get("parameters").get("media_storage_connection_id")
            chat_id = self.chat.id
            query = self.tool_usage_json.get("parameters").get("query")
            type = self.tool_usage_json.get("parameters").get("type")
            file_paths = self.tool_usage_json.get("parameters").get("file_paths")

            media_storage_response, file_uris, image_uris = execute_storage_query(
                connection_id=connection_id, chat_id=chat_id, execution_type=type, file_paths=file_paths, query=query
            )
            # Convert the tool response to a string and pretty format
            response_raw_str = json.dumps(media_storage_response, sort_keys=True, default=str)
            tool_response += response_raw_str
        ##################################################
        # ...

        ##################################################
        # IF NO TOOL IS FOUND WITH THE GIVEN NAME
        else:
            return f"""
                There is no tool with the name: {tool_name} in the system. Please make sure you are defining
                the correct tool name in the tool_usage_json.
            """, tool_name
        ##################################################

        tool_response += f"""
            '''
        """

        print("TOOL RESPONSE: ", tool_response)
        return tool_response, tool_name, file_uris, image_uris
