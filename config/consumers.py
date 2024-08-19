import json
from channels.generic.websocket import AsyncWebsocketConsumer


class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'logs'

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
