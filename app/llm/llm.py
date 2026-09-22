# app/llm/llm.py
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_core")
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)

from langchain_openai import ChatOpenAI


def get_llm():
    """
    创建聊天模型实例（走硅基流动的 OpenAI 兼容接口）
    :return: ChatOpenAI 实例
    """
    api_key = os.getenv("SILICONFLOW_API_KEY")
    base_url = os.getenv("SILICONFLOW_BASE_URL")
    model = os.getenv("CHAT_MODEL", "deepseek-ai/DeepSeek-V3")

    if not api_key:
        raise ValueError(f"未找到 SILICONFLOW_API_KEY，请检查 {ENV_PATH}")

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=0.7,
        timeout=60,
    )