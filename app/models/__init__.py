# -*- coding: utf-8 -*-
"""app.models 包：接口用到的请求 / 响应数据模型。

前端和后端之间用 JSON 传递数据，这里用 Pydantic 的 BaseModel
定义"数据长什么样"，FastAPI 会自动帮我们做参数校验。
"""
# 1. 导包
from pydantic import BaseModel


# 2. 请求模型：前端提问时发过来的数据
class ChatRequest(BaseModel):
    """聊天请求体。"""
    question: str          # 用户问的问题
    session_id: str = ""   # 会话编号，用于多轮记忆（不传也能跑）


# 3. 响应模型：后端返回给前端的数据
class ChatResponse(BaseModel):
    """聊天响应体。"""
    answer: str            # 大模型生成的回答
    session_id: str = ""   # 回传会话编号，前端下次请求带上它
