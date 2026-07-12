import os

from langsmith import Client

from app.core.settings import settings


os.environ["LANGCHAIN_TRACING_V2"] = str(
    settings.LANGCHAIN_TRACING_V2
)

os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGCHAIN_ENDPOINT

os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY

os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT

print("========== LangSmith Loaded ==========")
print(os.environ["LANGCHAIN_PROJECT"])
client = Client()