from apps._services.image_generation.image_variation_executor import ImageVariationExecutor
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat


def execute_image_variation(assistant_id, chat_id, image_uri, image_size):
    assistant = Assistant.objects.get(id=assistant_id)
    chat = MultimodalChat.objects.get(id=chat_id)
    executor = ImageVariationExecutor(assistant=assistant, chat=chat)
    print(f"[image_variation_execution_handler.execute_image_variation] Executing image variation.")
    if assistant.image_generation_capability is False:
        return "[image_variation_execution_handler.execute_image_variation] This assistant is not authorized to create variations of images. The assistant must first be edited to allow image generation capabilities to be able to use this tool."

    try:
        response = executor.execute_variate_image(image_uri=image_uri, image_size=image_size)
    except Exception as e:
        error = f"[image_variation_execution_handler.execute_image_variation] Error occurred while creating variations of the image: {str(e)}"
        return error
    print(f"[image_variation_execution_handler.execute_image_variation] Image variations created successfully.")
    return response
