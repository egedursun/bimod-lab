#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: deepseek_r1.py
#  Last Modified: 2025-01-31 17:15:03
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-01-31 17:15:04
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


import replicate
from typing import List
import os

from apps.core.generative_ai.magroute import (
    DEEPSEEK_MODEL_NAME
)

from apps.core.generative_ai.utils import (
    ChatRoles
)

from apps.multimodal_chat.utils import (
    transmit_websocket_log,
)
from config.settings import INTERNAL_REPLICATE_API_KEY


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
            def _build_prompt(
                structured_list: List[dict]
            ) -> str:
                open_source_prompt = """
                    ---
                    # Prompts & Conversation History:
                    ---

                    **Important Notes:**

                    - Do NOT provide your response in the form of prompts, simply deliver your answer without any
                    formatting regarding role/content key specifications.

                    ---
                """
                for i, prompt in enumerate(structured_list):
                    role = prompt["role"]
                    content = prompt["content"]

                    open_source_prompt += f"""
                    [{i}] {role}: {content}
                    """

                return open_source_prompt

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
                os.environ["REPLICATE_API_TOKEN"] = INTERNAL_REPLICATE_API_KEY

                prompt = DeepSeekR1.chat.completions._build_prompt(
                    structured_list=messages
                )

                current_thought_accumulation, response = "", ""
                think_mode = False

                for event in replicate.stream(
                    DEEPSEEK_MODEL_NAME,
                    input={
                        "prompt": str(prompt),
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "top_p": top_p,
                        "frequency_penalty": frequency_penalty,
                        "presence_penalty": presence_penalty
                    }
                ):

                    event_chunk = str(event)

                    if DeepSeekR1.ModeSpecifiers.THINK_START in str(event):
                        event_chunk = event_chunk.replace(
                            DeepSeekR1.ModeSpecifiers.THINK_START,
                            ""
                        )
                        think_mode = True

                    if DeepSeekR1.ModeSpecifiers.THINK_END in str(event):
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
                            DeepSeekR1.SentenceTerminals.PERIOD in event_chunk or
                            DeepSeekR1.SentenceTerminals.QUESTION in event_chunk or
                            DeepSeekR1.SentenceTerminals.EXCLAMATION in event_chunk
                        ):

                            if DeepSeekR1.SentenceTerminals.PERIOD in event_chunk:
                                current_thought_accumulation += event_chunk.split(
                                    DeepSeekR1.SentenceTerminals.PERIOD
                                )[0] + DeepSeekR1.SentenceTerminals.PERIOD

                            elif DeepSeekR1.SentenceTerminals.EXCLAMATION in event_chunk:
                                current_thought_accumulation += event_chunk.split(
                                    DeepSeekR1.SentenceTerminals.EXCLAMATION
                                )[0] + DeepSeekR1.SentenceTerminals.EXCLAMATION

                            elif DeepSeekR1.SentenceTerminals.QUESTION in event_chunk:
                                current_thought_accumulation += event_chunk.split(
                                    DeepSeekR1.SentenceTerminals.QUESTION
                                )[0] + DeepSeekR1.SentenceTerminals.QUESTION

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

                            ############################
                            # Reset the buffer
                            ############################
                            current_thought_accumulation = ""
                            if DeepSeekR1.SentenceTerminals.PERIOD in event_chunk:
                                if len(event_chunk.split(DeepSeekR1.SentenceTerminals.PERIOD)) > 1:
                                    current_thought_accumulation += event_chunk.split(
                                        DeepSeekR1.SentenceTerminals.PERIOD
                                    )[1]

                            elif DeepSeekR1.SentenceTerminals.EXCLAMATION in event_chunk:
                                if len(event_chunk.split(DeepSeekR1.SentenceTerminals.EXCLAMATION)) > 1:
                                    current_thought_accumulation += event_chunk.split(
                                        DeepSeekR1.SentenceTerminals.EXCLAMATION
                                    )[1]

                            elif DeepSeekR1.SentenceTerminals.QUESTION in event_chunk:
                                if len(event_chunk.split(DeepSeekR1.SentenceTerminals.QUESTION)) > 1:
                                    current_thought_accumulation += event_chunk.split(
                                        DeepSeekR1.SentenceTerminals.QUESTION
                                    )[1]

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

