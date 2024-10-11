#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: harmoniq_executor.py
#  Last Modified: 2024-10-07 03:01:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-07 03:04:19
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
import time
import wave
from io import BytesIO

from asgiref.sync import async_to_sync

from apps.core.harmoniq.utils import (
    DEFAULT_HARMONIQ_MODEL, DEFAULT_HARMONIQ_VOICE, DEFAULT_PCM_SAMPLING_RATE,
    DEFAULT_PCM_BITS_PER_SAMPLE, DEFAULT_PCM_NUMBER_OF_CHANNELS, get_tool_usage_instructions_prompt,
    get_available_tools_prompt)

import base64
import websockets
import json

from apps.harmoniq.models import Harmoniq
from apps.harmoniq.utils import HARMONIQ_DEITIES_INSTRUCTIONS_MAP
from apps.llm_core.models import LLMCore


class OpenAIRealtimeAPIClient:
    def __init__(self, harmoniq_agent: Harmoniq, llm_model: LLMCore):
        self.harmoniq_agent = harmoniq_agent
        self.llm_model = llm_model
        self.websocket_url = f"wss://api.openai.com/v1/realtime?model={DEFAULT_HARMONIQ_MODEL}"
        self.audio_buffer = b""
        self.transcript = ""

    async def connect(self):
        self.ws = await websockets.connect(
            self.websocket_url,
            extra_headers={
                "Authorization": f"Bearer {self.llm_model.api_key}",
                "OpenAI-Beta": "realtime=v1"
            })

    async def send_message(self, message):
        harmoniq_deity = self.harmoniq_agent.harmoniq_deity
        harmoniq_deity_instructions = HARMONIQ_DEITIES_INSTRUCTIONS_MAP.get(harmoniq_deity, "")
        optional_instructions = self.harmoniq_agent.optional_instructions

        formal_message = f"""
            ---
            **Your Identity: {self.harmoniq_agent.name}**
            **Your Main Instructions:**
            '''
            {harmoniq_deity_instructions}
            '''
            **Additional Instructions (neglect if no content):**
            '''
            {optional_instructions}
            '''
            ---
            **Tool Usage Instructions:**
            '''
            {get_tool_usage_instructions_prompt()}
            '''
            ---
            **Available Tools:**
            '''
            {get_available_tools_prompt(harmoniq_agent=self.harmoniq_agent)}
            '''
            ---
            **USER'S QUERY / MESSAGE TO YOU:**
            '''
            {message}
            '''
            ---
        """
        event = {"type": "conversation.item.create",
                 "item": {
                     "type": "message",
                     "role": "user",
                     "content": [{"type": "input_text", "text": formal_message}]
                 }}
        await self.ws.send(json.dumps(event))

    async def create_response(self):
        event = {
            "type": "response.create",
            "response": {
                "modalities": ["audio", "text"],  # Request both audio and text response
                "voice": DEFAULT_HARMONIQ_VOICE
        }}
        await self.ws.send(json.dumps(event))

    async def receive_audio_response(self):
        audio_done = False
        transcript_done = False
        text_done = False
        last_message_time = time.time()
        timeout = 10

        while True:
            try:
                response = await asyncio.wait_for(self.ws.recv(), timeout=timeout)
                data = json.loads(response)
                if data.get('type') == 'response.audio.delta':
                    audio_base64 = data.get('delta', '')
                    if audio_base64:
                        decoded_chunk = base64.b64decode(audio_base64)
                        self.audio_buffer += decoded_chunk
                    last_message_time = time.time()

                elif data.get('type') == 'response.audio_transcript.delta':
                    transcript_delta = data.get('delta', '')
                    if transcript_delta:
                        self.transcript += transcript_delta
                    last_message_time = time.time()

                elif data.get('type') == 'response.audio.done':
                    audio_done = True
                    audio_base64 = data.get('delta', '')
                    if audio_base64:
                        decoded_chunk = base64.b64decode(audio_base64)
                        self.audio_buffer += decoded_chunk
                    last_message_time = time.time()

                elif data.get('type') == 'response.audio_transcript.done':
                    transcript_done = True
                    transcript_delta = data.get('delta', '')
                    if transcript_delta:
                        self.transcript += transcript_delta
                    last_message_time = time.time()

                elif data.get('type') == 'response.text.done':
                    text_done = True

            except asyncio.TimeoutError:
                if audio_done and transcript_done and (time.time() - last_message_time) >= timeout:
                    await self.ws.close()
                    wav_data = pcm_to_wav(self.audio_buffer)
                    self.audio_buffer = wav_data
                    break

    async def request_communication(self, query_text: str = None):
            await self.connect()
            if query_text:
                await self.send_message(query_text)
                await self.create_response()
            await self.receive_audio_response()


def sync_request_communication(api_client, query_text):
    async_to_sync(api_client.request_communication)(query_text)


def pcm_to_wav(pcm_data, num_channels=DEFAULT_PCM_NUMBER_OF_CHANNELS, sample_rate=DEFAULT_PCM_SAMPLING_RATE,
               bits_per_sample=DEFAULT_PCM_BITS_PER_SAMPLE):
    byte_depth = bits_per_sample // 8
    wav_output = BytesIO()
    with wave.open(wav_output, 'wb') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(byte_depth)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm_data)
    return wav_output.getvalue()

