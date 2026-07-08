from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.settings import settings


class GeminiLLM:

    _llm = None

    @classmethod
    def get_llm(cls):

        if cls._llm is None:

            cls._llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0,
                model_kwargs={
                    "response_mime_type": "application/json"
                }
            )

        return cls._llm