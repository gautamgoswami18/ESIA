from langsmith import traceable
from core.settings import settings
@traceable
def hello(name):
    return f"Hello {name}"
print(settings.LANGCHAIN_TRACING_V2)
print(settings.LANGCHAIN_PROJECT)
print(settings.LANGCHAIN_ENDPOINT)
print(settings.LANGCHAIN_API_KEY)
print(hello("Gautam"))