# -*- coding: utf-8 -*-
"""环节3：向量化 —— 接入硅基流动的 embedding 模型，把文字变成向量"""
import os
from langchain_openai import OpenAIEmbeddings


def get_embeddings():
    """返回 embedding 模型对象，供切分后的文本块向量化使用"""
    api_key = os.getenv("SILICONFLOW_API_KEY")
    if not api_key:
        raise ValueError("未找到 SILICONFLOW_API_KEY，请先配置硅基流动的密钥")

    return OpenAIEmbeddings(
        model=os.getenv("EMBEDDING_MODEL", "BAAI/bge-large-zh-v1.5"),
        api_key=api_key,
        base_url=os.getenv("SILICONFLOW_BASE_URL"),
        # bge 模型不是 OpenAI 的，跳过它自带的长度检查，避免误报
        check_embedding_ctx_length=False,
    )
