# -*- coding: utf-8 -*-
"""
RAG 核心链路（组长负责）
流程：加载 → 切分 → 向量化 → 存储 → 检索
"""
import os
from dotenv import load_dotenv

# 项目根目录：本文件在 app/rag/ 下，往上三级就是 campus_rag 根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载 .env 里的密钥（如果 .env 不存在则静默跳过）
load_dotenv(os.path.join(BASE_DIR, ".env"))

# 资料目录 和 向量库存放目录
DATA_DIR = os.path.join(BASE_DIR, "data")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")
