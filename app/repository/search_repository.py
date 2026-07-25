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

        collection_size = self.collection.count()
        if collection_size == 0:
            return {
                "ids": [[]],
                "metadatas": [[]],
                "documents": [[]],
                "distances": [[]],
            }

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, collection_size),
            include=["documents", "metadatas", "distances"],
        )

        return results

    def get_employee_documents(
        self,
        employee_id: int,
    ) -> list[str]:
        result = self.collection.get(
            where={"employee_id": employee_id},
            include=["documents"],
        )
        return [
            str(document)
            for document in (result.get("documents") or [])
            if document
        ]
