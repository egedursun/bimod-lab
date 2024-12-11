#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: orchestration_history_builder.py
#  Last Modified: 2024-10-05 02:25:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
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

from apps.core.system_prompts.chat_history_factory_builder import (
    HistoryBuilder
)

from apps.orchestrations.models import (
    OrchestrationQuery,
    OrchestrationQueryLog
)

import base64 as b64

from apps.orchestrations.utils import (
    OrchestrationQueryLogTypesNames
)

logger = logging.getLogger(__name__)


class OrchestrationHistoryBuilder:

    @staticmethod
    def build(query_chat: OrchestrationQuery):
        chat_messages: list[OrchestrationQueryLog] = query_chat.logs.all().order_by("created_at")
        context_history = []

        for log in chat_messages:
            sender_type = log.log_type

            if sender_type == OrchestrationQueryLogTypesNames.USER:
                sender_type = HistoryBuilder.ChatRoles.USER

                message_text_content = f"""
                **User's Direct Query:**

                Direction: User --> Orchestrator
                Target Subject: Orchestrator

                    ```
                    {log.log_text_content}
                    ```
                """

            elif sender_type == OrchestrationQueryLogTypesNames.WORKER_REQUEST:
                sender_type = HistoryBuilder.ChatRoles.ASSISTANT

                message_text_content = f"""
                **Orchestrator's REQUEST to the Worker:**

                Direction: Orchestrator --> Worker
                Target Subject: Worker
                * Worker ID: {log.context_worker.id}
                * Worker Name: {log.context_worker.name}

                ```
                {log.log_text_content}
                ```
                """

            elif sender_type == OrchestrationQueryLogTypesNames.WORKER_RESPONSE:
                sender_type = HistoryBuilder.ChatRoles.ASSISTANT

                message_text_content = f"""
                **Worker's RESPONSE to the Orchestrator:**

                Direction: Worker --> Orchestrator
                Target Subject: Orchestrator
                * Worker ID: {log.context_worker.id}
                * Worker Name: {log.context_worker.name}

                ```
                {log.log_text_content}
                ```
                """

            elif sender_type == OrchestrationQueryLogTypesNames.INFO:
                sender_type = HistoryBuilder.ChatRoles.ASSISTANT

                message_text_content = f"""
                **Orchestration Process - Information Log:**

                Direction: System --> Orchestrator
                Target Subject: Orchestrator
                Provider: Orchestration Management System - Information Logging Provider

                ```
                {log.log_text_content}
                ```
                """

            elif sender_type == OrchestrationQueryLogTypesNames.ERROR:
                sender_type = HistoryBuilder.ChatRoles.ASSISTANT

                message_text_content = f"""
                **[!] Orchestration Process - Error Log:**

                Direction: System --> Orchestrator
                Target Subject: Orchestrator
                Provider: Orchestration Management System - Error Logging Provider

                ```
                {log.log_text_content}
                ```
                """

            elif sender_type == OrchestrationQueryLogTypesNames.MAESTRO_ANSWER:
                sender_type = HistoryBuilder.ChatRoles.ASSISTANT
                message_text_content = log.log_text_content

            else:
                logger.error(f"[OrchestrationHistoryBuilder.build] Unknown log type: {sender_type}")
                continue

            message_image_urls = log.log_image_contents
            message_file_urls = log.log_file_contents

            message_object = {
                "role": sender_type.lower()
            }

            content_wrapper = [
                {
                    "type": "text",
                    "text": message_text_content
                }
            ]

            if message_image_urls and sender_type == HistoryBuilder.ChatRoles.USER:

                for image_url in message_image_urls:
                    # get the object from local storage
                    full_uri = f"{image_url}"

                    try:
                        # download image from URL
                        response = requests.get(full_uri)

                        # read the file
                        image_bytes = response.content
                        image_b64 = b64.b64encode(image_bytes).decode("utf-8")

                    except Exception as e:
                        logger.error(f"[OrchestrationHistoryBuilder.build] Error while downloading the image: {e}")
                        continue

                    image_content_wrapper = {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{image_url.split('.')[-1]};base64,{image_b64}"
                        }
                    }

                    image_uri_info_wrapper = {
                        "type": "text",
                        "text": f"Detected Image URLs: {image_url}"
                    }

                    content_wrapper.append(image_content_wrapper)
                    content_wrapper.append(image_uri_info_wrapper)

            if message_file_urls and sender_type == HistoryBuilder.ChatRoles.USER:

                for file_url in message_file_urls:
                    # get the object from local storage
                    file_uri_info_wrapper = {
                        "type": "text",
                        "text": f"Detected File URLs: {file_url}"
                    }

                    content_wrapper.append(file_uri_info_wrapper)

            message_object["content"] = content_wrapper

            if sender_type != HistoryBuilder.ChatRoles.SYSTEM:
                context_history.append(message_object)

        logger.info(f"[OrchestrationHistoryBuilder.build] Built the context history for the Orchestration Query.")

        return context_history
