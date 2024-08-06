from apps._services.image_generation.image_modification_executor import ImageModificationExecutor
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat


def execute_image_modification(assistant_id, chat_id, prompt, edit_image_uri, edit_image_mask_uri, image_size):
    assistant = Assistant.objects.get(id=assistant_id)
    chat = MultimodalChat.objects.get(id=chat_id)
    executor = ImageModificationExecutor(assistant=assistant, chat=chat)
    print(f"[image_modification_execution_handler.execute_image_modification] Executing image modification.")
    if assistant.image_generation_capability is False:
        error = "[image_modification_execution_handler.execute_image_modification] This assistant is not authorized to modify images. The assistant must first be edited to allow image generation capabilities to be able to use this tool."
        return error

    try:
        response = executor.execute_modify_image(prompt=prompt, edit_image_uri=edit_image_uri,
                                                 edit_image_mask_uri=edit_image_mask_uri, image_size=image_size)
    except Exception as e:
        error = f"[image_modification_execution_handler.execute_image_modification] Error occurred while modifying the image: {str(e)}"
        return error
    print(f"[image_modification_execution_handler.execute_image_modification] Image modified successfully.")
    return response
