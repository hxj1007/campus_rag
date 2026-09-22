# -*- coding: utf-8 -*-
"""
校园资料智能问答助手 —— FastAPI 后端入口
运行方式：python main.py   （或用 uvicorn main:app --reload）
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# 创建 FastAPI 服务实例
app = FastAPI(
    title="校园资料智能问答助手",
    description="基于 RAG 的校园资料问答后端服务",
    version="1.0.0",
)

# CORS 跨域配置（前端 index.html 要访问后端，必须加，否则浏览器会拦截）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求模型：前端发来的数据格式
class ChatRequest(BaseModel):
    question: str  # 用户的问题


# 响应模型：返回给前端的数据格式
class ChatResponse(BaseModel):
    answer: str  # 助手的回答


@app.get("/")
def root():
    """根路径，用来测试后端是否启动成功"""
    return {
        "message": "校园资料智能问答助手后端已启动",
        "接口文档": "/docs",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    问答接口（核心）
    TODO: 组长在这里接入 RAG 检索（app/rag/），成员3 在这里接入大模型（app/llm/）
    目前先返回一句话，证明接口能跑通。
    """
    # 下面这两行是占位代码，等 RAG 和模型层做好后替换掉
    answer = "接口已通！你刚才问的是：" + req.question + "（RAG 链路待接入）"
    return ChatResponse(answer=answer)


if __name__ == "__main__":
    # 启动服务，浏览器访问 http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
