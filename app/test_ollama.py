from app.llm.ollama_provider import OllamaProvider

provider = OllamaProvider()

response = provider.generate(
    "Who are you?"
)

print(response)