import google.generativeai as genai

from app.core.settings import settings
from app.llm.base_provider import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):

    def __init__(self):

        genai.configure(
            api_key=settings.GOOGLE_API_KEY
        )

        self.model = genai.GenerativeModel(
            settings.GEMINI_MODEL
        )

    def generate(
        self,
        prompt: str,
        json_mode: bool = False
    ) -> str:

        if json_mode:
            prompt = (
                "Return ONLY valid JSON.\n\n"
                + prompt
            )

        response = self.model.generate_content(
            prompt
        )

        return response.text.strip()