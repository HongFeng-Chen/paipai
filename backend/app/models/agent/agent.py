from rag.rag_engine import RAGEngine
from prompts.templates import PromptManager
from .schemas import AgentInput, AgentOutput
from typing import Optional

class Agent:
    def __init__(self, rag_engine: RAGEngine, prompt_manager: PromptManager, llm_callable=None):
        """
        :param rag_engine: 已初始化的 RAG 引擎
        :param prompt_manager: 提示词管理器
        :param llm_callable: 一个可调用对象，接收提示字符串，返回回答文本
        """
        self.rag = rag_engine
        self.prompts = prompt_manager
        self.llm = llm_callable or self._mock_llm

    def _mock_llm(self, prompt: str) -> str:
        """模拟 LLM 调用（开发测试用）"""
        return f"[模拟回答] 基于提示: {prompt[:50]}..."

    def run(self, user_input: AgentInput) -> AgentOutput:
        """
        执行 Agent 工作流：
        1. 如果需要 RAG，检索相关上下文
        2. 选择合适的提示模板
        3. 构造最终提示
        4. 调用 LLM 生成回答
        """
        sources = []
        context = ""

        if user_input.use_rag:
            # 检索相关文档块
            retrieved = self.rag.retrieve(user_input.query, user_input.top_k)
            sources = retrieved
            # 拼接上下文
            context = "\n---\n".join([item["text"] for item in retrieved])

        # 选择提示模板并渲染
        if context:
            # 有上下文时使用 QA 模板
            prompt = self.prompts.render(
                "qa_with_context",
                context=context,
                question=user_input.query
            )
        else:
            # 无上下文时可能使用通用 QA 模板（需提前定义）
            prompt = self.prompts.render(
                "general_qa",
                question=user_input.query
            )

        # 调用 LLM
        answer = self.llm(prompt)

        return AgentOutput(
            answer=answer,
            sources=sources,
            metadata={"prompt_used": prompt}  # 可选，调试用
        )