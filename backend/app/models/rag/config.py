from pydantic_settings import BaseSettings
from typing import Optional

class RAGConfig(BaseSettings):
    # Qdrant 配置
    qdrant_location: str = ":memory:"  # 支持 ":memory:", 路径, 或 URL
    collection_name: str = "documents"
    vector_size: int = 384  # 与嵌入模型匹配
    distance: str = "Cosine"  # 距离度量

    # 嵌入模型配置
    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 500
    chunk_overlap: int = 0  # 简单分块，无重叠

    class Config:
        env_prefix = "RAG_"  # 可从环境变量覆盖，如 RAG_QDRANT_LOCATION