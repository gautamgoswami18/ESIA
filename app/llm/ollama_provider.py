import ollama

from app.core.settings import settings
from app.llm.base_provider import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):

    def __init__(self):
        self.model = settings.OLLAMA_MODEL

    def generate(
        self,
        prompt: str,
        json_mode: bool = False
    ) -> str:

        kwargs = {}

        if json_mode:
            kwargs["format"] = "json"

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            **kwargs
        )

        return response["message"]["content"].strip()