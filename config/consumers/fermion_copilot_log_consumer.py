#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: fermion_copilot_log_consumer.py
#  Last Modified: 2024-11-28 20:27:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-28 20:27:30
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import json
import logging

from channels.generic.websocket import (
    AsyncWebsocketConsumer
)

from config.settings import (
    BASE_URL
)

logger = logging.getLogger(__name__)


class APIExportTypesNames:
    ASSISTANT = "assistant"
    LEANMOD = "leanmod"
    ORCHESTRATION = "orchestration"
    VOIDFORGER = "voidforger"

    @staticmethod
    def as_list():
        return [
            APIExportTypesNames.ASSISTANT,
            APIExportTypesNames.LEANMOD,
            APIExportTypesNames.ORCHESTRATION,
            APIExportTypesNames.VOIDFORGER,
        ]


class FermionLogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        connection_type = self.scope['url_route']['kwargs']['connection_type']

        self.group_name = f'logs_{connection_type}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def send_log(self, event):
        log_message = event['message']

        await self.send(
            text_data=json.dumps(
                {
                    'log': log_message
                }
            )
        )

    @staticmethod
    def clean_endpoint(
        export_type: str,
        raw_endpoint: str
    ):

        # Remove "http://localhost:8000" or "https://bimod.io" from the endpoint

        clean_endpoint = raw_endpoint.replace(
            BASE_URL,
            ""
        )

        # Remove "/app" from the endpoint (e.g. "/app/export_assistants/... to "/export_assistants/...")

        clean_endpoint = clean_endpoint.split("/app")[1]

        # Remove the export type from the endpoint (e.g. "/export_assistants/..." to "/...")

        if export_type == APIExportTypesNames.ASSISTANT:
            clean_endpoint = clean_endpoint.replace(
                "/export_assistants/exported/voidforger_assistants",
                ""
            )

        elif export_type == APIExportTypesNames.LEANMOD:
            clean_endpoint = clean_endpoint.replace(
                "/export_leanmods/exported/voidforger_assistants",
                ""
            )

        elif export_type == APIExportTypesNames.ORCHESTRATION:
            clean_endpoint = clean_endpoint.replace(
                "/export_orchestrations/exported/voidforger_assistants",
                ""
            )

        elif export_type == APIExportTypesNames.VOIDFORGER:
            clean_endpoint = clean_endpoint.replace(
                "/export_voidforger/exported/voidforger_assistants",
                ""
            )

        else:
            pass

        # Make sure the endpoint does not start with "/"

        if clean_endpoint and clean_endpoint[0] == "/":
            clean_endpoint = clean_endpoint[1:]

        # Make sure the endpoint does not end with "/"

        if clean_endpoint and clean_endpoint[-1] == "/":
            clean_endpoint = clean_endpoint[:-1]

        # Replace "/" with "-" in the endpoint (e.g. "/.../.../... to "-...-...-...")

        clean_endpoint = clean_endpoint.replace(
            "/",
            "-"
        )

        return clean_endpoint
