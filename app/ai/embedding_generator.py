from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """
    Generates vector embeddings from resume text.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def generate_embedding(self, text: str) -> list[float]:
        """
        Convert text into embedding vector.
        """

        if not text:
            return []

        embedding = self.model.encode(text)

        return embedding.tolist()