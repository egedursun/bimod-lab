#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: image_generator_execution_handler.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: image_generator_execution_handler.py
#  Last Modified: 2024-09-25 17:51:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:14:25
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.image_generation.image_generator_executor import ImageGeneratorExecutor
from apps.assistants.models import Assistant
from apps.multimodal_chat.models import MultimodalChat


def execute_image_generation(assistant_id, chat_id, prompt, image_size, quality):
    assistant = Assistant.objects.get(id=assistant_id)
    chat = MultimodalChat.objects.get(id=chat_id)
    executor = ImageGeneratorExecutor(assistant=assistant, chat=chat)
    print(f"[image_generator_execution_handler.execute_image_generation] Executing image generation.")
    if assistant.image_generation_capability is False:
        return ("[image_generator_execution_handler.execute_image_generation] This assistant is not authorized to "
                "generate images. The assistant must first be edited to allow generating images to be able to use "
                "this tool.")
    try:
        response = executor.execute_generate_image(prompt=prompt, image_size=image_size, quality=quality)
    except Exception as e:
        error = (f"[image_generator_execution_handler.execute_image_generation] Error occurred while generating the "
                 f"image: {str(e)}")
        return error
    print(f"[image_generator_execution_handler.execute_image_generation] Image generated successfully.")
    return response
