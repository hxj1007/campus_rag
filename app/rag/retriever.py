# -*- coding: utf-8 -*-
"""环节5：检索 —— 根据问题找出最相关的资料片段"""
from app.rag.vector_store import get_vector_store


def retrieve(question, k=4):
    """输入一个问题，返回最相关的 k 个文本片段（字符串列表）"""
    db = get_vector_store()
    docs = db.similarity_search(question, k=k)
    return [doc.page_content for doc in docs]
