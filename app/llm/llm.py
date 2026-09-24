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
    创建聊天模型实例（走 DeepSeek 官方接口）
    说明：大模型用 DeepSeek，embedding 用硅基流动，两者分开。
         DeepSeek 不提供 embedding，所以向量化单独走硅基流动。

    需要的环境变量（.env）：
        DEEPSEEK_API_KEY   DeepSeek 密钥
        DEEPSEEK_BASE_URL  https://api.deepseek.com
        DEEPSEEK_MODEL     聊天模型名（deepseek-chat）

    :return: ChatOpenAI 实例
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    base_url = os.getenv("DEEPSEEK_BASE_URL")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    if not api_key:
        raise ValueError(f"未找到 DEEPSEEK_API_KEY，请检查 {ENV_PATH}")
    if not base_url:
        raise ValueError(f"未找到 DEEPSEEK_BASE_URL，请检查 {ENV_PATH}")

    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=0.7,
        timeout=60,
    )