# -*- coding: utf-8 -*-
"""环节4：存储 —— 把向量存到 Chroma 本地向量库"""
from langchain_chroma import Chroma
from app.rag import CHROMA_DIR
from app.rag.embedding import get_embeddings


def build_vector_store(chunks):
    """把切分好的文本块向量化，并存入 chroma_db/ 目录"""
    Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=CHROMA_DIR,
    )
    print(f"已入库 {len(chunks)} 个文本块，存放在 {CHROMA_DIR}")


def get_vector_store():
    """连接已经建好的向量库（只读取，不重复入库）"""
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=get_embeddings(),
    )
