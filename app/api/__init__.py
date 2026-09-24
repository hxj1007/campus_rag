# -*- coding: utf-8 -*-
"""
大模型层（王皓阳负责）
职责：大模型接入 + 提示词 + 多轮记忆
对外提供 3 个最常用的入口，方便 main.py 直接引用：
    - get_llm        创建大模型实例
    - generate       RAG 生成主入口
    - ConversationMemory  多轮对话记忆
"""
# 1. 加载 .env 里的密钥（整个 llm 包共用一个入口，避免每个文件重复写）
import os
from dotenv import load_dotenv

# 项目根目录：本文件在 app/llm/ 下，往上两级就是 campus_rag 根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载 .env（如果 .env 不存在就静默跳过，不报错）
load_dotenv(os.path.join(BASE_DIR, ".env"))

# 2. 对外暴露常用对象（这样 main.py 可以写 from app.llm import generate）
from app.llm.llm import get_llm
from app.llm.generator import generate
from app.llm.memory import ConversationMemory