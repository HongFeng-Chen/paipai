from qdrant_client import QdrantClient
from qdrant_client.http import models
from .config import RAGConfig

class QdrantWrapper:
    def __init__(self, config: RAGConfig):
        self.config = config
        self.client = QdrantClient(location=config.qdrant_location)
        self._ensure_collection()

    def _ensure_collection(self):
        """确保集合存在，若不存在则创建"""
        collections = self.client.get_collections().collections
        if not any(c.name == self.config.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.config.collection_name,
                vectors_config=models.VectorParams(
                    size=self.config.vector_size,
                    distance=getattr(models.Distance, self.config.distance.upper())
                )
            )

    def upsert_points(self, points: list[models.PointStruct]):
        """批量插入点"""
        self.client.upsert(
            collection_name=self.config.collection_name,
            points=points
        )

    def search(self, query_vector: list[float], top_k: int) -> list[models.ScoredPoint]:
        """向量检索"""
        return self.client.search(
            collection_name=self.config.collection_name,
            query_vector=query_vector,
            limit=top_k
        )

    def delete_collection(self):
        """清理集合（可选）"""
        self.client.delete_collection(self.config.collection_name)