from app.ai.prompt import RAG_PROMPT
from app.ai.prompt import SUMMARY_PROMPT
from app.ai.prompt import COMPARE_PROMPT
from app.ai.search_grounding import (
    build_ranked_context,
    ground_search_response,
)
from app.llm.provider_factory import ProviderFactory
from app.services.search_service import SearchService
from app.utils.json_parser import JsonParser
from app.ai.query_normalizer import QueryNormalizer
from langsmith import traceable

class RAGChain:

    def __init__(self, db=None):
        self.search_service = SearchService(db=db)
        self.llm = ProviderFactory.get_provider()
    @traceable(name="Resume Search")
    def ask(
        self,
        question: str,
        top_k: int = 3
    ):

        normalized_query = QueryNormalizer.normalize(question)
        candidates = self.search_service.search_resumes(
            query=normalized_query,
            top_k=top_k,
        )

        if not candidates:
            return ground_search_response(question, [], None)

        prompt = RAG_PROMPT.format(
            context=build_ranked_context(candidates),
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

        generated = JsonParser.parse(response)
        return ground_search_response(
            question,
            candidates,
            generated,
        )

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
