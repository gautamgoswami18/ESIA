import chromadb

from app.ai.embedding_generator import EmbeddingGenerator


class SearchRepository:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )

        self.collection = self.client.get_collection(
            name="employee_resumes"
        )

        self.embedding_generator = EmbeddingGenerator()

    def search_resumes(
        self,
        query: str,
        top_k: int = 5
    ):

        query_embedding = self.embedding_generator.generate_embedding(
            query
        )

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results