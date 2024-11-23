#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: dream_manager.py
#  Last Modified: 2024-10-08 22:35:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-08 22:35:05
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

from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.core.visual_client.utils import dream_save_images_and_return_uris
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames


logger = logging.getLogger(__name__)


class DreamManager:

    def __init__(
        self,
        assistant,
        chat
    ):
        self.assistant = assistant
        self.chat = chat

    def dream_image_execution_manager(
        self,
        image_uri,
        image_size
    ):

        from apps.core.generative_ai.auxiliary_clients.auxiliary_llm_visual_client import AuxiliaryLLMVisualClient
        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles

        try:
            llm_c = AuxiliaryLLMVisualClient(
                assistant=self.assistant,
                chat_object=self.chat
            )
            logger.info("LLM Visual Client initialized.")

        except Exception as e:
            logger.error(f"Error occurred while initializing the LLM Visual Client: {e}")
            return None

        try:
            llm_output = llm_c.dream_image(
                image_uri=image_uri,
                image_size=image_size
            )

            if llm_output["success"] is False:
                logger.error(f"Error occurred while generating the image: {llm_output['message']}")
                return llm_output

        except Exception as e:

            logger.error(f"Error occurred while generating the image: {e}")
            return {
                "success": False,
                "message": "Error occurred on generating the image.",
                "image_url": None
            }

        if llm_output["image_url"]:

            img_llm_uri = llm_output["image_url"]

            try:
                logger.info(f"Downloading the image variation from: {img_llm_uri}")
                img_data = requests.get(img_llm_uri).content

            except Exception as e:

                logger.error(f"Error occurred while downloading the image variation: {e}")
                return {
                    "success": False,
                    "message": "Error occurred while downloading the image variation",
                    "image_url": None
                }

            try:
                tx = LLMTransaction(
                    organization=self.chat.assistant.organization,
                    model=self.chat.assistant.llm_model,
                    responsible_user=self.chat.user,
                    responsible_assistant=self.chat.assistant,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                    llm_cost=InternalServiceCosts.ImageVariation.COST,
                    transaction_type=ChatRoles.SYSTEM,
                    transaction_source=LLMTransactionSourcesTypesNames.VARIATE_IMAGE,
                    is_tool_cost=True
                )
                tx.save()
                logger.info(f"Transaction created for image variation: {tx.id}")

            except Exception as e:

                logger.error(f"Error occurred while saving the transaction: {e}")
                return {
                    "success": False,
                    "message": "Error occurred while saving the transaction.",
                    "image_url": None
                }

            if img_data:

                logger.info("Saving the image variation and returning the URI.")
                image_uri = dream_save_images_and_return_uris([img_data])[0]
                return {
                    "success": True,
                    "message": "",
                    "image_uri": image_uri
                }

        logger.error("Error occurred while downloading the image variation resulting file.")
        return {
            "success": False,
            "message": "Error occurred while downloading the image variation resulting file.",
            "image_url": None
        }
