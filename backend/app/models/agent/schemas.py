from pydantic import BaseModel
from typing import List, Optional, Any

class AgentInput(BaseModel):
    query: str
    top_k: int = 3
    use_rag: bool = True  # 控制是否使用 RAG

class AgentOutput(BaseModel):
    answer: str
    sources: List[dict] = []
    metadata: dict = {}