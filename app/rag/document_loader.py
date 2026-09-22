# -*- coding: utf-8 -*-
"""环节1：加载 —— 读取 data/ 目录下的所有 txt 资料"""
import os
from langchain_community.document_loaders import TextLoader
from app.rag import DATA_DIR


def load_documents():
    """把 data/ 目录下所有 .txt 文件读成 Document 列表"""
    documents = []
    for filename in os.listdir(DATA_DIR):
        # 只处理 txt 文件，跳过其它格式
        if not filename.endswith(".txt"):
            continue
        path = os.path.join(DATA_DIR, filename)
        loader = TextLoader(path, encoding="utf-8")
        documents.extend(loader.load())
    return documents
