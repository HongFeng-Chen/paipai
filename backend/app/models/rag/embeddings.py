from sentence_transformers import SentenceTransformer
from .config import RAGConfig

class EmbeddingModel:
    def __init__(self, config: RAGConfig):
        self.model = SentenceTransformer(config.embedding_model)
        self.vector_size = config.vector_size

    def encode(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()

    def encode_batch(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts).tolist()