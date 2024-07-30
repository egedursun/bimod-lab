from apps._services.image_generation.image_generator_executor import ImageGeneratorExecutor
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat


def execute_image_generation(assistant_id, chat_id, prompt, image_size, quality):
    assistant = Assistant.objects.get(id=assistant_id)
    chat = MultimodalChat.objects.get(id=chat_id)
    executor = ImageGeneratorExecutor(assistant=assistant, chat=chat)

    if assistant.image_generation_capability is False:
        return ("This assistant is not authorized to generate images. The assistant must first be edited to allow"
                "generating images to be able to use this tool.")

    try:
        response = executor.execute_generate_image(prompt=prompt, image_size=image_size, quality=quality)
    except Exception as e:
        print(f"Error occurred while generating the image: {str(e)}")
        return f"Error occurred while generating the image: {str(e)}"
    return response
