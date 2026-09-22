# app/llm/embeddings.py
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_core")
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)

from langchain_openai import OpenAIEmbeddings


def get_embeddings():
    """
    创建硅基流动 embedding 模型实例（OpenAI 兼容接口）
    模型：BAAI/bge-large-zh-v1.5
    :return: OpenAIEmbeddings 实例
    """
    api_key = os.getenv("SILICONFLOW_API_KEY")
    base_url = os.getenv("SILICONFLOW_BASE_URL")
    model = os.getenv("EMBEDDING_MODEL", "BAAI/bge-large-zh-v1.5")

    if not api_key:
        raise ValueError(f"未找到 SILICONFLOW_API_KEY，请检查 {ENV_PATH}")

    return OpenAIEmbeddings(
        model=model,
        api_key=api_key,
        base_url=base_url,
        check_embedding_ctx_length=False,
    )