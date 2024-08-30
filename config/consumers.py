import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from apps._meta.voidforger.test_helpers.generator import generate_for_time_step
from apps.multimodal_chat.utils import BIMOD_STREAMING_END_TAG
import random as r


class OrchestrationGenericLogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        maestro_id = self.scope['url_route']['kwargs']['maestro_id']
        self.group_name = f'orchestration_generic_logs_{maestro_id}'

        # Join the logs group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the logs group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming messages from the client if needed
        pass

    async def send_log(self, event):
        # Send the log message to the WebSocket
        log_message = event['message']
        await self.send(text_data=json.dumps({
            'log': log_message
        }))


class OrchestrationLogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_id = self.scope['url_route']['kwargs']['query_id']
        self.group_name = f'orchestration_logs_{query_id}'

        # Join the logs group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the logs group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming messages from the client if needed
        pass

    async def send_log(self, event):
        # Send the log message to the WebSocket
        log_message = event['message']
        await self.send(text_data=json.dumps({
            'log': log_message
        }))


class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.group_name = f'logs_{chat_id}'

        # Join the logs group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the logs group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming messages from the client if needed
        pass

    async def send_log(self, event):
        # Send the log message to the WebSocket
        log_message = event['message']
        await self.send(text_data=json.dumps({
            'log': log_message
        }))


#####


class VoidForgeOperationLogsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = f'voidforge_operation_logs'

        # Join the logs group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        await self.send_log()

    async def disconnect(self, close_code):
        # Leave the logs group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming messages from the client if needed
        pass

    async def send_log(self):
        while True:
            sleep_time_random = r.randint(1, 1)
            log_dict = generate_for_time_step()
            await self.send(text_data=json.dumps({
                'log': log_dict
            }))
            await self.send(text_data=json.dumps({
                'log': BIMOD_STREAMING_END_TAG
            }))
            await asyncio.sleep(sleep_time_random)

