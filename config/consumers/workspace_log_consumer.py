#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: workspace_log_consumer.py
#  Last Modified: 2024-11-16 05:16:49
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 05:17:00
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

from channels.generic.websocket import (
    AsyncWebsocketConsumer
)


class WorkspaceLogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        voidforger_chat_id = self.scope['url_route']['kwargs']['voidforger_chat_id']
        self.group_name = f'voidforger_logs_{voidforger_chat_id}'

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
