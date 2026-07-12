import json

from app.ai.chroma_service import ChromaService
from app.ai.embedding_generator import EmbeddingGenerator
from app.ai.prompt import RAG_PROMPT
from app.schemas.ai_response import AIResponse
from app.ai.prompt import SUMMARY_PROMPT
from app.ai.prompt import COMPARE_PROMPT
from app.llm.provider_factory import ProviderFactory
from app.utils.json_parser import JsonParser
from app.ai.query_normalizer import QueryNormalizer
from langsmith import traceable

class RAGChain:

    def __init__(self):
        self.chroma = ChromaService()
        self.llm = ProviderFactory.get_provider()
    @traceable(name="Resume Search")
    def ask(
        self,
        question: str,
        top_k: int = 3
    ):

        # Create embedding
        normalized_query = QueryNormalizer.normalize(question)
        embedding = EmbeddingGenerator.generate_embedding(normalized_query)

        # Search Chroma
        results = self.chroma.search(
            query_embedding=embedding,
            top_k=top_k
        )

        documents = results.get("documents", [])

        if not documents:

            return {
                "query": question,
                "best_candidate": {},
                "rank": 0,
                "reason": "No matching resume found.",
                "other_candidates": []
            }

        context = "\n\n".join(documents[0])

        prompt = RAG_PROMPT.format(
            context=context,
            question=question
        )

        response = self.llm.generate(
            prompt,
            json_mode=True
        )

        print("=" * 80)
        print("RAW SEARCH RESPONSE")
        print(response)
        print("=" * 80)

        return JsonParser.parse(response)

    @traceable(name="Resume Summary")
    def summarize_resume(
        self,
        resume_text: str
    ) -> str:

        prompt = SUMMARY_PROMPT.format(
            resume=resume_text
        )

        response = self.llm.generate(
            prompt,
            json_mode=False
        )

        return response.strip()
    
    
    @traceable(name="Candidate Comparison")
    def compare_candidates(
        self,
        resume1: str,
        resume2: str
    ) -> str:
    
        prompt = COMPARE_PROMPT.format(
            resume1=resume1,
            resume2=resume2
        )
    
        response = self.llm.generate(
            prompt,
            json_mode=False
        )
    
        return response.strip()