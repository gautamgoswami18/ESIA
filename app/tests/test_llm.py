from app.ai.llm import GeminiLLM

llm = GeminiLLM.get_llm()

response = llm.invoke(
    "Introduce yourself in one sentence."
)

print(response.content)