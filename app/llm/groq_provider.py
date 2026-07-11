from groq import Groq

from app.core.settings import settings
from app.llm.base_provider import BaseLLMProvider


class GroqProvider(BaseLLMProvider):

    def __init__(self):
        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL

    def generate(
        self,
        prompt: str,
        json_mode: bool = False
    ) -> str:

        messages = []

        if json_mode:
            messages.append(
                {
                    "role": "system",
                    "content": (
                        "You are a JSON API."
                        " Always return valid JSON."
                        " Never use markdown."
                    )
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        request = {
            "model": self.model,
            "messages": messages,
            "temperature": 0
        }

        if json_mode:
            request["response_format"] = {
                "type": "json_object"
            }

        response = self.client.chat.completions.create(
            **request
        )

        return response.choices[0].message.content.strip()