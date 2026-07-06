import chromadb


class ChromaService:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="employee_resumes"
        )

    def add_resume(
        self,
        employee_id: int,
        resume_text: str,
        embedding: list[float]
    ):

        self.collection.upsert(
            ids=[str(employee_id)],
            documents=[resume_text],
            embeddings=[embedding],
            metadatas=[
                {
                    "employee_id": employee_id
                }
            ]
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5
    ):

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )