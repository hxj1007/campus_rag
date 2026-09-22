# -*- coding: utf-8 -*-
"""环节2：切分 —— 把长文档切成小块，方便向量化和检索"""
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    """把文档切成约 500 字的小块，块之间重叠 50 字，避免一句话被截断"""
    splitter = RecursiveCharacterTextSplitter(
        # 分隔符优先级：先按段落、换行，再按中文标点，最后才按字符硬切
        separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""],
        chunk_size=500,      # 每个文本块的最大字符数
        chunk_overlap=50,    # 相邻块之间的重叠字符数
    )
    return splitter.split_documents(documents)
