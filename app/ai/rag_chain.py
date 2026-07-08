import json

from app.ai.chroma_service import ChromaService
from app.ai.embedding_generator import EmbeddingGenerator
from app.ai.llm import GeminiLLM
from app.ai.prompt import RAG_PROMPT
from app.schemas.ai_response import AIResponse
from app.ai.prompt import SUMMARY_PROMPT
from app.ai.prompt import COMPARE_PROMPT


class RAGChain:

    def __init__(self):
        self.chroma = ChromaService()
        self.llm = GeminiLLM.get_llm()

    def ask(
        self,
        question: str,
        top_k: int = 3
    ) -> AIResponse:

        # Generate embedding for user question
        question_embedding = EmbeddingGenerator.generate_embedding(question)

        # Search similar resumes from ChromaDB
        results = self.chroma.search(
            query_embedding=question_embedding,
            top_k=top_k
        )

        documents = results.get("documents", [])

        if not documents or not documents[0]:
            return AIResponse.model_validate(
                {
                    "query": question,
                    "best_candidate": {
                        "rank": 0,
                        "name": "",
                        "role": "",
                        "experience": "",
                        "match_score": 0,
                        "matching_skills": [],
                        "reason": "No matching resume found."
                    },
                    "other_candidates": [],
                    "recommendation": "No suitable candidate found."
                }
            )

        context = "\n\n".join(documents[0])

        prompt = RAG_PROMPT.format(
            context=context,
            question=question
        )

        response = self.llm.invoke(prompt)

        raw_response = response.content.strip()

        print("=" * 80)
        print("Gemini Raw Response")
        print(raw_response)
        print("=" * 80)

        # Remove markdown if Gemini returns ```json ... ```
        if raw_response.startswith("```json"):
            raw_response = raw_response.replace("```json", "")
            raw_response = raw_response.replace("```", "").strip()

        elif raw_response.startswith("```"):
            raw_response = raw_response.replace("```", "").strip()

        try:
            data = json.loads(raw_response)

            print("=" * 80)
            print("Parsed JSON")
            print(data)
            print("=" * 80)

            # Some Gemini responses wrap everything inside search_result
            if "search_result" in data:
                data = data["search_result"]

            return AIResponse.model_validate(data)

        except Exception as ex:
            print("=" * 80)
            print("JSON Parsing Error")
            print(ex)
            print(raw_response)
            print("=" * 80)
            raise ex
        

    def summarize_resume(
        self,
        resume_text: str
    ) -> str:
        prompt = SUMMARY_PROMPT.format(
            resume=resume_text
        )
        response = self.llm.invoke(prompt)
        return response.content.strip()
    
    
    def compare_candidates(
        self,
        resume1: str,
        resume2: str
    ):

        prompt = COMPARE_PROMPT.format(
            resume1=resume1,
            resume2=resume2
        )

        response = self.llm.invoke(prompt)

        return response.content.strip()