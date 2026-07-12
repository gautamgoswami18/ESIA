from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingGenerator:

    _model = None
    _langchain_embeddings = None

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

    @classmethod
    def get_langchain_embeddings(cls):

        if cls._langchain_embeddings is None:

            cls._langchain_embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

        return cls._langchain_embeddings