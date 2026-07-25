from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.ai.base_rag import BaseRAG
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

class LangChainRAG(BaseRAG):

    def __init__(self, db=None):

        self.llm = ProviderFactory.get_provider().get_langchain_llm()
        self.search_service = SearchService(db=db)

        self.prompt = ChatPromptTemplate.from_template(
            RAG_PROMPT
        )

        self.search_chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(
        self,
        question: str,
        top_k: int = 3,
    ):
        candidates = self.search_service.search_resumes(
            query=question,
            top_k=top_k,
        )
        if not candidates:
            return ground_search_response(question, [], None)

        response = self.search_chain.invoke(
            {
                "context": build_ranked_context(candidates),
                "question": question,
            }
        )
        generated = JsonParser.parse(response)
        return ground_search_response(
            question,
            candidates,
            generated,
        )
      

    def summarize_resume(
        self,
        resume_text: str
    ):

        prompt = ChatPromptTemplate.from_template(
            SUMMARY_PROMPT
        )

        chain = (
            prompt
            | self.llm
            | StrOutputParser()
        )

        return chain.invoke(
            {
                "resume": resume_text
            }
        ).strip()
    def compare_candidates(
        self,
        resume1: str,
        resume2: str
    ):
    
        prompt = ChatPromptTemplate.from_template(
            COMPARE_PROMPT
        )
    
        chain = (
            prompt
            | self.llm
            | StrOutputParser()
        )
    
        return chain.invoke(
            {
                "resume1": resume1,
                "resume2": resume2
            }
        ).strip()
