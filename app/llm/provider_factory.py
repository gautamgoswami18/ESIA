from app.core.settings import settings


class ProviderFactory:

    @staticmethod
    def get_provider():

        provider = settings.LLM_PROVIDER.lower()

        if provider == "groq":
            from app.llm.groq_provider import GroqProvider
            return GroqProvider()

        elif provider == "gemini":
            from app.llm.gemini_provider import GeminiProvider
            return GeminiProvider()

        elif provider == "ollama":
            from app.llm.ollama_provider import OllamaProvider
            return OllamaProvider()

        raise ValueError(f"Unsupported provider: {provider}")