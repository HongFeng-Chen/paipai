import uuid
from typing import List, Dict, Any
from qdrant_client.models import PointStruct
from .config import RAGConfig

class DocumentProcessor:
    def __init__(self, config: RAGConfig):
        self.chunk_size = config.chunk_size

    def chunk_text(self, text: str) -> List[str]:
        """简单按字符分块（可根据需求改进）"""
        return [text[i:i+self.chunk_size] for i in range(0, len(text), self.chunk_size)]

    def create_points(self, text: str, metadata: Dict[str, Any], embed_func) -> List[PointStruct]:
        """将文本分块并生成向量点"""
        chunks = self.chunk_text(text)
        points = []
        for idx, chunk in enumerate(chunks):
            vector = embed_func(chunk)
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": chunk,
                    "chunk_index": idx,
                    **metadata
                }
            )
            points.append(point)
        return points