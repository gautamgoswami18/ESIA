from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:
            cls._model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2"
            )

        return cls._model

    @classmethod
    def generate_embedding(
        cls,
        text: str
    ) -> list[float]:

        model = cls.get_model()

        return model.encode(text).tolist()