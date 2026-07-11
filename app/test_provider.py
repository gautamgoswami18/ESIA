from app.llm.provider_factory import ProviderFactory

provider = ProviderFactory.get_provider()

response = provider.generate(
    "Return only this JSON:\n"
    '{"message":"Hello ESIA"}'
)

print(response)