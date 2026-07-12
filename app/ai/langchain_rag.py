from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from app.ai.base_rag import BaseRAG
from app.ai.embedding_generator import EmbeddingGenerator
from app.ai.prompt import RAG_PROMPT
from app.ai.prompt import SUMMARY_PROMPT
from app.ai.prompt import COMPARE_PROMPT
from app.llm.provider_factory import ProviderFactory
from app.utils.json_parser import JsonParser

class LangChainRAG(BaseRAG):

    def __init__(self):

        self.embedding = EmbeddingGenerator.get_langchain_embeddings()

        self.llm = ProviderFactory.get_provider().get_langchain_llm()

        self.vectorstore = Chroma(
            persist_directory="./chroma_db",
            collection_name="employee_resumes",
            embedding_function=self.embedding
        )

        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={
                "k": 5
            }
        )

        self.prompt = ChatPromptTemplate.from_template(
            RAG_PROMPT
        )

        self.search_chain = (
            {
                "context": self.retriever,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(
        self,
        question: str
    ):

        response = self.search_chain.invoke(question)
        return JsonParser.parse(response)
      

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
   