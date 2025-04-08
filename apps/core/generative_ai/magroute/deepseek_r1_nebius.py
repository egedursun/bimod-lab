#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: deepseek_r1_nebius.py
#  Last Modified: 2025-02-03 11:18:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-02-03 11:18:48
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from typing import List

from openai import OpenAI

from apps.core.generative_ai.magroute import DEEPSEEK_MODEL_NAME__NEBIUS
from apps.core.generative_ai.utils import (
    ChatRoles
)
from apps.multimodal_chat.utils import transmit_websocket_log
from config.settings import INTERNAL_NEBIUS_API_KEY


class DeepSeekR1:
    class ModeSpecifiers:
        THINK_START = "<think>"
        THINK_END = "</think>"

    class SentenceTerminals:
        PERIOD = ". "
        EXCLAMATION = "! "
        QUESTION = "? "

    class chat:
        class completions:

            @staticmethod
            def create(
                chat_id: str,
                messages: List[dict],
                socket_type: str,
                max_tokens: float = 1_000_000,
                temperature: float = 0.1,
                top_p: float = 1.0,
                frequency_penalty: float = 0.0,
                presence_penalty: float = 0.0,
                fermion__is_fermion_supervised: bool = False,
                fermion__export_type: str = "",
                fermion__endpoint: str = ""
            ):

                current_thought_accumulation, response = "", ""
                think_mode = False

                c = OpenAI(
                    base_url="https://api.studio.nebius.ai/v1/",
                    api_key=INTERNAL_NEBIUS_API_KEY,
                )

                for message in messages:
                    if message.get("role") == "developer":
                        message["role"] = "system"
                        message["content"] += """
                            ---
                            Please share your response without any formatting regarding role/content key specifications.
                            ---
                        """

                for event in c.chat.completions.create(
                    model=DEEPSEEK_MODEL_NAME__NEBIUS,
                    stream=True,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty
                ):

                    event_chunk = str(event.choices[0].delta.content)

                    if DeepSeekR1.ModeSpecifiers.THINK_START in event_chunk:
                        event_chunk = event_chunk.replace(
                            DeepSeekR1.ModeSpecifiers.THINK_START,
                            ""
                        )
                        think_mode = True

                    if DeepSeekR1.ModeSpecifiers.THINK_END in event_chunk:
                        think_parts = event_chunk.split(
                            DeepSeekR1.ModeSpecifiers.THINK_END
                        )
                        if len(think_parts) > 1:
                            event_chunk = think_parts[1]
                        else:
                            event_chunk = ""

                        think_mode = False

                    if think_mode is True:

                        if (
                            event_chunk == "." or
                            event_chunk == "?" or
                            event_chunk == "!"
                        ):

                            if event_chunk == ".":
                                current_thought_accumulation += "."

                            elif event_chunk == "!":
                                current_thought_accumulation += "!"

                            elif event_chunk == "?":
                                current_thought_accumulation += "?"

                            ############################
                            # Stream the socket message
                            ############################
                            transmit_websocket_log(
                                f"""🧠 {current_thought_accumulation}""",
                                chat_id=chat_id,
                                sender_type=socket_type,
                                fermion__is_fermion_supervised=fermion__is_fermion_supervised,
                                fermion__export_type=fermion__export_type,
                                fermion__endpoint=fermion__endpoint
                            )
                            ############################

                            current_thought_accumulation = ""

                        else:
                            ############################
                            # Get the final response
                            ############################
                            current_thought_accumulation += event_chunk

                    else:
                        response += event_chunk

                #################################
                # Mock client response structure
                #################################

                class MockMessage:
                    def __init__(self, role: str, content: str):
                        self.role = role
                        self.content = content

                class MockMessageWrapper:
                    def __init__(self, message: MockMessage):
                        self.message = message

                class MockResponse:
                    def __init__(self, choices: List[MockMessageWrapper]):
                        self.choices = choices

                response = MockResponse(
                    choices=[
                        MockMessageWrapper(
                            message=MockMessage(
                                role=ChatRoles.ASSISTANT,
                                content=response
                            )
                        )
                    ]
                )

                return response
