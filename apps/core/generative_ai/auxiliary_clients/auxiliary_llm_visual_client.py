#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auxiliary_llm_visual_client.py
#  Last Modified: 2024-10-09 01:02:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 01:02:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

import requests
from openai import OpenAI

from apps.core.generative_ai.auxiliary_methods.errors.error_log_prompts import (
    get_image_generation_error_log,
    get_image_modification_error_log,
    get_image_variation_error_log
)

from apps.core.generative_ai.utils import (
    DEFAULT_IMAGE_GENERATION_MODEL,
    DefaultImageResolutionChoices,
    DefaultImageQualityChoices,
    DEFAULT_IMAGE_GENERATION_N,
    DEFAULT_IMAGE_MODIFICATION_MODEL,
    DEFAULT_IMAGE_MODIFICATION_N,
    DEFAULT_IMAGE_VARIATION_MODEL,
    DEFAULT_IMAGE_VARIATION_N
)

from apps.core.generative_ai.utils import (
    DefaultImageResolutionChoicesNames,
    DefaultImageQualityChoicesNames
)

logger = logging.getLogger(__name__)


class AuxiliaryLLMVisualClient:

    def __init__(
        self,
        assistant,
        chat_object
    ):
        self.assistant = assistant
        self.chat = chat_object

        self.connection = OpenAI(
            api_key=assistant.llm_model.api_key
        )

    def generate_image(
        self,
        prompt: str,
        image_size: str,
        quality: str
    ):
        final_output = {
            "success": False,
            "message": "",
            "image_url": ""
        }

        gen_img_llm_model = DEFAULT_IMAGE_GENERATION_MODEL

        if image_size == DefaultImageResolutionChoicesNames.SQUARE:
            image_size = DefaultImageResolutionChoices.Min1024Max1792.SQUARE

        elif image_size == DefaultImageResolutionChoicesNames.PORTRAIT:
            image_size = DefaultImageResolutionChoices.Min1024Max1792.PORTRAIT

        elif image_size == DefaultImageResolutionChoicesNames.LANDSCAPE:
            image_size = DefaultImageResolutionChoices.Min1024Max1792.LANDSCAPE

        else:
            image_size = DefaultImageResolutionChoices.Min1024Max1792.SQUARE

        if quality == DefaultImageQualityChoicesNames.STANDARD:
            quality = DefaultImageQualityChoices.STANDARD

        elif quality == DefaultImageQualityChoicesNames.HIGH_DEFINITION:
            quality = DefaultImageQualityChoices.HIGH_DEFINITION

        else:
            quality = DefaultImageQualityChoices.STANDARD

        try:
            gen_img_output = self.connection.images.generate(
                model=gen_img_llm_model,
                prompt=prompt,
                size=image_size,
                quality=quality,
                n=DEFAULT_IMAGE_GENERATION_N
            )

            image_url = gen_img_output.data[0].url
            final_output["success"] = True
            final_output["image_url"] = image_url
            logger.info(f"Generated image at: {image_url}")

            return final_output

        except Exception as e:
            logger.error(f"Failed to generate image: {str(e)}")
            final_output["message"] = get_image_generation_error_log(error_logs=str(e))

            return final_output

    def edit_image(
        self,
        prompt: str,
        edit_image_uri: str,
        edit_image_mask_uri: str,
        image_size: str
    ):

        final_output = {
            "success": False,
            "message": "",
            "image_url": ""
        }

        edit_img_llm_model = DEFAULT_IMAGE_MODIFICATION_MODEL

        if image_size == DefaultImageResolutionChoicesNames.SQUARE:
            image_size = DefaultImageResolutionChoices.Min1024Max1792.SQUARE

        elif image_size == DefaultImageResolutionChoicesNames.PORTRAIT:
            image_size = DefaultImageResolutionChoices.Min1024Max1792.PORTRAIT

        elif image_size == DefaultImageResolutionChoicesNames.LANDSCAPE:
            image_size = DefaultImageResolutionChoices.Min1024Max1792.LANDSCAPE

        else:
            image_size = DefaultImageResolutionChoices.Min1024Max1792.SQUARE

        try:
            edit_img = requests.get(edit_image_uri)
            mask_img = requests.get(edit_image_mask_uri)
            edit_img_bytes = edit_img.content
            mask_img_bytes = mask_img.content

            llm_output = self.connection.images.edit(
                model=edit_img_llm_model,
                image=edit_img_bytes,
                mask=mask_img_bytes,
                prompt=prompt,
                n=DEFAULT_IMAGE_MODIFICATION_N,
                size=image_size
            )

            img_url = llm_output.data[0].url

            final_output["success"] = True
            final_output["image_url"] = img_url
            logger.info(f"Edited image at: {img_url}")

            return final_output

        except Exception as e:
            logger.error(f"Failed to edit image: {str(e)}")
            final_output["message"] = get_image_modification_error_log(error_logs=str(e))

            return final_output

    def dream_image(
        self,
        image_uri: str,
        image_size: str
    ):

        final_output = {
            "success": False,
            "message": "",
            "image_url": ""
        }

        dream_img_llm_model = DEFAULT_IMAGE_VARIATION_MODEL

        if image_size == DefaultImageResolutionChoicesNames.SQUARE:
            image_size = DefaultImageResolutionChoices.Min1024Max1792.SQUARE

        elif image_size == DefaultImageResolutionChoicesNames.PORTRAIT:
            image_size = DefaultImageResolutionChoices.Min1024Max1792.PORTRAIT

        elif image_size == DefaultImageResolutionChoicesNames.LANDSCAPE:
            image_size = DefaultImageResolutionChoices.Min1024Max1792.LANDSCAPE

        else:
            image_size = DefaultImageResolutionChoices.Min1024Max1792.SQUARE

        try:

            img = requests.get(image_uri)
            img_bytes = img.content

            output = self.connection.images.create_variation(
                model=dream_img_llm_model,
                image=img_bytes,
                n=DEFAULT_IMAGE_VARIATION_N,
                size=image_size
            )

            img_url = output.data[0].url
            final_output["success"] = True
            final_output["image_url"] = img_url
            logger.info(f"Dreamed image at: {img_url}")

        except Exception as e:
            logger.error(f"Failed to dream image: {str(e)}")

            final_output["message"] = get_image_variation_error_log(
                error_logs=str(e)
            )

            return final_output

        return final_output
