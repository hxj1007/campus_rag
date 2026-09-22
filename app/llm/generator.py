# app/llm/generator.py
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_core")
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)

from langchain_core.messages import HumanMessage, SystemMessage

from app.llm.llm import get_llm
from app.llm.prompt import SYSTEM_PROMPT, format_context
from app.llm.memory import history_to_messages


# 全局唯一的 LLM 实例（懒加载 + 缓存）
_llm = None


def _get_cached_llm():
    """缓存 LLM 实例，避免每次调用都重新创建"""
    global _llm
    if _llm is None:
        _llm = get_llm()
    return _llm


def generate(context, question, history=None):
    """
    RAG 生成主入口（供 FastAPI 后端 /chat 接口调用）
    :param context: 检索到的上下文（str 或 Document 列表）
    :param question: 用户当前问题
    :param history: 历史对话 [{"role":"user"/"assistant","content":"..."}]
    :return: str，模型生成的回答
    """
    if history is None:
        history = []

    # 兼容 Document 列表
    if isinstance(context, (list, tuple)):
        context = format_context(context)
    elif context is None:
        context = "（无相关参考资料）"

    # 组装消息：System(带上下文) + 历史 + 当前问题
    messages = [
        SystemMessage(content=SYSTEM_PROMPT.format(context=context))
    ]
    messages.extend(history_to_messages(history))
    messages.append(HumanMessage(content=question))

    # 调用模型
    response = _get_cached_llm().invoke(messages)
    return response.content