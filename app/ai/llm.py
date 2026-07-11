from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq

from app.core.settings import settings


class LLMFactory:

    _llm = None

    @classmethod
    def get_llm(cls):

        if cls._llm is not None:
            return cls._llm

        provider = settings.LLM_PROVIDER.lower()

        if provider == "gemini":

            cls._llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0,
                model_kwargs={
                    "response_mime_type": "application/json"
                }
            )

        elif provider == "groq":

            cls._llm = ChatGroq(
                model=settings.GROQ_MODEL,
                api_key=settings.GROQ_API_KEY,
                temperature=0
            )

        elif provider == "ollama":

            cls._llm = ChatOllama(
                model=settings.OLLAMA_MODEL,
                base_url=settings.OLLAMA_BASE_URL,
                temperature=0,
                format="json"
            )

        else:
            raise ValueError(
                f"Unsupported LLM Provider: {provider}"
            )

        return cls._llm