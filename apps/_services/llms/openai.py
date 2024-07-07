
from openai import OpenAI


class InternalOpenAIClient:
    def __init__(self, llm_core, assistant):
        self.connection = OpenAI(
            api_key="sk-1234567890"
        )
