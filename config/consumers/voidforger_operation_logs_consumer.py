#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: voidforger_operation_logs_consumer.py
#  Last Modified: 2024-10-09 19:31:20
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:31:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


import asyncio
import json
import random as r

from channels.generic.websocket import AsyncWebsocketConsumer

from apps._meta.voidforger.test_helpers.generator import generate_for_time_step
from apps.multimodal_chat.utils import BIMOD_STREAMING_END_TAG


class VoidForgeOperationLogsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = f'voidforge_operation_logs'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_log()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_log(self):
        while True:
            sleep_time_random = r.randint(1, 1)
            log_dict = generate_for_time_step()
            await self.send(text_data=json.dumps({'log': log_dict}))
            await self.send(text_data=json.dumps({'log': BIMOD_STREAMING_END_TAG}))
            await asyncio.sleep(sleep_time_random)
