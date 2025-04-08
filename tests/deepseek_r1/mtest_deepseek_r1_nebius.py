#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: mtest_deepseek_r1_nebius.py
#  Last Modified: 2025-02-03 10:58:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-02-03 10:58:48
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

from apps.core.generative_ai.utils import (
    ChatRoles
)


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
                    **Prompts & Conversation History:**

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
                NEBIUS_API_TOKEN = (
                    "eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXB"
                    "vX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnb29nbGUtb2F1d"
                    "GgyfDEwMTExNzE5NTAyMzQyODg3MTQxMSIsInNjb3BlIjoib3BlbmlkIG9mZmxpbm"
                    "VfYWNjZXNzIiwiaXNzIjoiYXBpX2tleV9pc3N1ZXIiLCJhdWQiOlsiaHR0cHM6Ly9"
                    "uZWJpdXMtaW5mZXJlbmNlLmV1LmF1dGgwLmNvbS9hcGkvdjIvIl0sImV4cCI6MTg5"
                    "NjAxNTMyMCwidXVpZCI6ImJmNmMwZWMxLTlkNmUtNGI2NS1hZjdiLTEyMzY2NTQ1M"
                    "TA4YiIsIm5hbWUiOiJiaW1vZCIsImV4cGlyZXNfYXQiOiIyMDMwLTAxLTMwVDE0Oj"
                    "U1OjIwKzAwMDAifQ.P4XZWLc_tUvwyI7djZpxU44X3nmoGfZ3UleersNZwk4"
                )

                prompt = DeepSeekR1.chat.completions._build_prompt(
                    structured_list=messages
                )

                current_thought_accumulation, response = "", ""
                think_mode = False

                """
                input={
                        "prompt": str(prompt),
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "top_p": top_p,
                        "frequency_penalty": frequency_penalty,
                        "presence_penalty": presence_penalty
                    }
                """

                c = OpenAI(
                    base_url="https://api.studio.nebius.ai/v1/",
                    api_key=NEBIUS_API_TOKEN,
                )

                for event in c.chat.completions.create(
                    model="deepseek-ai/DeepSeek-R1",
                    stream=True,
                    messages=messages
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
                            print("[WEBSOCKET LOG]: " + current_thought_accumulation)
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


if __name__ == "__main__":
    response = DeepSeekR1.chat.completions.create(
        chat_id="123",
        messages=[
            {
                "role": ChatRoles.USER,
                "content": "Explain the concept of death, use your internal reasoning tokens."
            },
        ],
        socket_type="websocket"
    )

    print(response.choices[0].message.content)
