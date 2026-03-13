from .config import RAGConfig
from .embeddings import EmbeddingModel
from .qdrant_client import QdrantWrapper
from .document_processor import DocumentProcessor
from typing import List, Dict, Any, Optional

class RAGEngine:
    def __init__(self, config: Optional[RAGConfig] = None):
        self.config = config or RAGConfig()
        self.embedder = EmbeddingModel(self.config)
        self.qdrant = QdrantWrapper(self.config)
        self.processor = DocumentProcessor(self.config)

    def add_document(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        """添加单个文档（自动分块、嵌入并存储）"""
        metadata = metadata or {}
        points = self.processor.create_points(
            text, 
            metadata, 
            self.embedder.encode  # 传入编码函数
        )
        self.qdrant.upsert_points(points)
        return len(points)

    def add_documents(self, docs: List[Dict[str, Any]]):
        """批量添加文档，每个元素包含 'text' 和可选的 'metadata'"""
        all_points = []
        for doc in docs:
            points = self.processor.create_points(
                doc["text"],
                doc.get("metadata", {}),
                self.embedder.encode
            )
            all_points.extend(points)
        self.qdrant.upsert_points(all_points)
        return len(all_points)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """检索相关文档块，返回包含文本和分数的列表"""
        query_vector = self.embedder.encode(query)
        results = self.qdrant.search(query_vector, top_k)
        return [
            {
                "text": hit.payload["text"],
                "score": hit.score,
                "metadata": {k: v for k, v in hit.payload.items() if k != "text"}
            }
            for hit in results
        ]

    def query(self, query: str, top_k: int = 3, generate_answer: bool = False) -> Dict[str, Any]:
        """检索并可选生成回答（生成函数需外部注入）"""
        sources = self.retrieve(query, top_k)
        context = "\n---\n".join([s["text"] for s in sources])
        answer = None
        if generate_answer:
            # 这里可以调用外部 LLM，或由调用方处理
            answer = f"基于以下信息：\n{context}\n\n回答：{query} 的相关信息如上。"
        return {
            "answer": answer,
            "sources": sources
        }