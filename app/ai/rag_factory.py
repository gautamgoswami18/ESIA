from app.core.settings import settings

from app.ai.rag_chain import RAGChain
from app.ai.langchain_rag import LangChainRAG


class RAGFactory:

    @staticmethod
    def get_rag(db=None):

        if settings.RAG_PROVIDER.lower() == "langchain":
            return LangChainRAG(db=db)

        return RAGChain(db=db)
