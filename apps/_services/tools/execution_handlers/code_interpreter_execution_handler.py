from apps._services.code_interpreter.code_interpreter_executor import CodeInterpreterExecutor
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat


def execute_code_interpreter(assistant_id, chat_id, file_paths, query):
    assistant = Assistant.objects.get(id=assistant_id)
    chat = MultimodalChat.objects.get(id=chat_id)
    executor = CodeInterpreterExecutor(assistant=assistant, chat=chat)
    try:
        response = executor.interpret_code(full_file_paths=file_paths, query_string=query)
    except Exception as e:
        print(f"[code_interpreter_execution_handler.execute_code_interpreter] Error occurred while interpreting the code: {str(e)}")
        return None, None, None
    file_uris = response.get("file_uris")
    image_uris = response.get("image_uris")
    return response, file_uris, image_uris
