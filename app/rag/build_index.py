# -*- coding: utf-8 -*-
"""
一键建库入口：加载 → 切分 → 向量化 → 存储
在项目根目录运行一次即可：python -m app.rag.build_index
"""
import os
from app.rag import CHROMA_DIR
from app.rag.document_loader import load_documents
from app.rag.text_splitter import split_documents
from app.rag.vector_store import build_vector_store


def build_index():
    """把 data/ 目录的资料处理成向量库；如果已经建过库就跳过"""
    # 先检查密钥有没有配置好，避免直接报底层错误
    if not os.getenv("SILICONFLOW_API_KEY"):
        print("还没有配置硅基流动的 API Key，无法向量化！")
        print("请先做两步：")
        print("  1) 把 .env.example 复制一份，改名为 .env")
        print("  2) 在 .env 里填入 SILICONFLOW_API_KEY（硅基流动官网免费申请）")
        return

    # 已经建过库就不再重复向量化（省时间、省 API 额度）
    if os.path.isdir(CHROMA_DIR) and os.listdir(CHROMA_DIR):
        print("向量库已存在，跳过建库。")
        print("若要重建（比如改了资料），请先删除 chroma_db/ 目录再运行本脚本。")
        return

    print("第 1 步：加载 data/ 目录下的资料 ...")
    docs = load_documents()
    print(f"  共加载 {len(docs)} 篇文档")

    print("第 2 步：切分文档 ...")
    chunks = split_documents(docs)
    print(f"  共切分 {len(chunks)} 个文本块")

    print("第 3 步：向量化并存入 Chroma ...")
    build_vector_store(chunks)

    print("建库完成！接下来可以在代码里用 retrieve() 检索了。")


if __name__ == "__main__":
    build_index()
