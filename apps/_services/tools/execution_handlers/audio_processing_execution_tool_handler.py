from apps._services.audio_processing.audio_processing_executor import AudioProcessingExecutor
from apps._services.audio_processing.utils import AudioProcessingExecutorActionsNames
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat


def execute_audio_processing_tool(assistant_id, chat_id, action, audio_file_path=None, text_content=None,
                                  voice_selection=None):
    assistant = Assistant.objects.get(id=assistant_id)
    chat = MultimodalChat.objects.get(id=chat_id)
    executor = AudioProcessingExecutor(assistant=assistant, chat=chat)

    print(f"[audio_processing_execution_tool_handler.execute_audio_processing_tool] Executing audio processing tool.")
    if action == AudioProcessingExecutorActionsNames.TTS:
        response = executor.convert_text_to_audio_file(text_content=text_content, voice_selection=voice_selection)
    elif action == AudioProcessingExecutorActionsNames.STT:
        response = executor.convert_audio_to_text(audio_file_path=audio_file_path)
    else:
        response = None

    print(f"[audio_processing_execution_tool_handler.execute_audio_processing_tool] Audio processing tool "
          f"executed successfully.")
    return response
