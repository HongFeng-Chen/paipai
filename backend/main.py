from fastapi import FastAPI
from pydantic import BaseModel
from rag.rag_engine import RAGEngine
from rag.config import RAGConfig
from prompts.templates import PromptManager
from agent.agent import Agent
from agent.schemas import AgentInput, AgentOutput

# 初始化各模块
rag_config = RAGConfig()  # 默认内存模式
rag_engine = RAGEngine(rag_config)

prompt_manager = PromptManager(file_path="prompts/prompts.toml")  # 或直接传入字典

# 可注入真实的 LLM 客户端，如 OpenAI
def real_llm(prompt: str) -> str:
    # 实际调用 OpenAI / 本地模型
    # from openai import OpenAI
    # client = OpenAI()
    # response = client.chat.completions.create(...)
    # return response.choices[0].message.content
    return f"真实 LLM 响应：{prompt[:100]}"

agent = Agent(
    rag_engine=rag_engine,
    prompt_manager=prompt_manager,
    llm_callable=real_llm  # 替换为真实 LLM
)

# FastAPI 应用
app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3
    use_rag: bool = True

class QueryResponse(BaseModel):
    answer: str
    sources: list

@app.post("/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    agent_input = AgentInput(
        query=request.query,
        top_k=request.top_k,
        use_rag=request.use_rag
    )
    output = agent.run(agent_input)
    return QueryResponse(answer=output.answer, sources=output.sources)

@app.post("/upload")
async def upload(text: str, metadata: dict = {}):
    chunks = rag_engine.add_document(text, metadata)
    return {"chunks": chunks}