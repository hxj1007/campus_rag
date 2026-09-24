# -*- coding: utf-8 -*-
"""embedding 实例（已合并到 rag 层，这里只引用，避免两处重复定义）。

原来的 get_embeddings() 在 app/rag/embedding.py 和 app/llm/embeddings.py 各有一份，
功能一样，容易改漏。现在统一只保留 app/rag/embedding.py 这一处，
这里直接引用它，老代码里写 from app.llm.embeddings import get_embeddings 也能用。
"""
from app.rag.embedding import get_embeddings
