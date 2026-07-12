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
            distance = distances[i]
            # Convert Chroma distance to percentage
            distance = distances[i]
            if distance <= 1:
                match_score = round((1 - distance) * 100)
            else:
                match_score = round(100 / (1 + distance))

            match_score = max(0, min(match_score, 100))
            
            response.append({

                "employee_id": metadatas[i].get("employee_id"),

                "distance": round(distances[i], 4),

                "match_score": match_score,                

                "resume_text": documents[i]

            })

        return response