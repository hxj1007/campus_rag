# -*- coding: utf-8 -*-
"""
校园资料智能问答助手 —— FastAPI 后端入口
运行方式：python main.py   （或用 uvicorn main:app --reload）
"""
# 1. 导包
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# 导入 RAG 检索（组长负责的链路）
from app.rag.retriever import retrieve
# 导入大模型生成（王皓阳负责的模型层）
from app.llm.generator import generate
# 导入多轮对话记忆
from app.llm.memory import ConversationMemory

# 2. 创建 FastAPI 服务实例
app = FastAPI(
    title="校园资料智能问答助手",
    description="基于 RAG 的校园资料问答后端服务",
    version="1.0.0",
)

# 3. CORS 跨域配置（前端 index.html 要访问后端，必须加，否则浏览器会拦截）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3.5 挂载前端静态文件目录，浏览器访问 /static/index.html 就能打开前端页面
app.mount("/static", StaticFiles(directory="static"), name="static")


# 4. 创建一个全局的多轮记忆对象（进程重启会清空，符合课程范围）
#    max_turns=5 表示每个会话最多记住最近 5 轮对话
memory = ConversationMemory(max_turns=5)


# 5. 请求模型：前端发来的数据格式
class ChatRequest(BaseModel):
    question: str          # 用户的问题
    session_id: str = ""   # 会话标识，用于区分不同用户/不同对话（不传也能跑）


# 6. 响应模型：返回给前端的数据格式
class ChatResponse(BaseModel):
    answer: str            # 助手的回答
    session_id: str = ""   # 回传会话标识，前端下次请求带上它


@app.get("/", response_class=HTMLResponse)
def root():
    """首页：显示一个可以点击进入前端页面的链接"""
    return """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>校园资料智能问答助手</title>
    </head>
    <body>
        <h2>校园资料智能问答助手 —— 后端已启动</h2>
        <p><a href="/static/index.html">点击进入前端问答页面</a></p>
        <p><a href="/docs">接口文档（/docs）</a></p>
    </body>
    </html>
    """


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    问答接口（核心）
    流程：检索资料 → 取历史 → 生成回答 → 存记忆 → 返回
    """
    # 1. 取出会话标识（前端没传就是空字符串，相当于所有请求共用一个会话）
    session_id = req.session_id

    # 2. 从向量库检索和问题最相关的资料片段（返回字符串列表）
    context = retrieve(req.question, k=4)

    # 3. 取出该会话之前的历史对话，交给大模型参考
    history = memory.get_history(session_id)

    # 4. 调用大模型生成回答（传入：资料 + 问题 + 历史）
    answer = generate(context, req.question, history)

    # 5. 把本轮问答存入记忆，供后续追问使用
    memory.add_user(session_id, req.question)
    memory.add_assistant(session_id, answer)

    # 6. 返回回答和会话标识
    return ChatResponse(answer=answer, session_id=session_id)


if __name__ == "__main__":
    # 启动服务，浏览器访问 http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
