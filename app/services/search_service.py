from app.repository.search_repository import SearchRepository


class SearchService:

    def __init__(self):
        self.repository = SearchRepository()

    def search_resumes(
        self,
        query: str,
        top_k: int = 5
    ):

        results = self.repository.search_resumes(
            query=query,
            top_k=top_k
        )

        response = []

        ids = results.get("ids", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for i in range(len(ids)):

            response.append({

                "employee_id": metadatas[i].get("employee_id"),

                "distance": round(distances[i], 4),

                "resume_text": documents[i]

            })

        return response