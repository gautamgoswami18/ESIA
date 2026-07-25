from groq import Groq
from langsmith import traceable
from langchain_groq import ChatGroq

from app.core.settings import settings
from app.llm.base_provider import BaseLLMProvider
from app.ai.prompt import build_resume_prompt
from app.utils.json_parser import JsonParser


class GroqProvider(BaseLLMProvider):

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL

    @traceable(name="Groq LLM")
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
                    "content":
                        "You are a JSON API. "
                        "Always return valid JSON. "
                        "Never use markdown."
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

    # ---------- NEW ----------
    def get_langchain_llm(self):

        return ChatGroq(
            model=self.model,
            api_key=settings.GROQ_API_KEY,
            temperature=0
        )
    


    def extract_resume_profile(
        self,
        resume_text: str
    ) -> dict:
    
        prompt = build_resume_prompt(resume_text)
    
        response = self.generate(prompt)
    
        return JsonParser.parse(response)