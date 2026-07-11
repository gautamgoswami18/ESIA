from app.llm.gemini_provider import GeminiProvider


provider = GeminiProvider()

response = provider.generate(
    "Say Hello"
)

print(response)