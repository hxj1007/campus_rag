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
    创建聊天模型实例（**统一走硅基流动的 OpenAI 兼容接口**）
    说明：硅基流动同时提供 chat 模型和 embedding 模型，
         所以 LLM 和 embedding 共用同一个 API Key 和 base_url。

    需要的环境变量（.env）：
        SILICONFLOW_API_KEY  硅基流动密钥
        SILICONFLOW_BASE_URL https://api.siliconflow.cn/v1
        CHAT_MODEL           聊天模型名（如 deepseek-ai/DeepSeek-V3）

    :return: ChatOpenAI 实例
    """
    api_key = os.getenv("SILICONFLOW_API_KEY")
    base_url = os.getenv("SILICONFLOW_BASE_URL")
    model = os.getenv("CHAT_MODEL", "deepseek-ai/DeepSeek-V3")

    if not api_key:
        raise ValueError(f"未找到 SILICONFLOW_API_KEY，请检查 {ENV_PATH}")
    if not base_url:
        raise ValueError(f"未找到 SILICONFLOW_BASE_URL，请检查 {ENV_PATH}")

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=0.7,
        timeout=60,
    )