# -*- coding: utf-8 -*-
"""
校园资料智能问答助手 —— FastAPI 后端入口
运行方式：python main.py   （或用 uvicorn main:app --reload）
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
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


# 校园资料所在目录
DATA_DIR = Path(__file__).parent / "data"

# 常见校园问题关键词，用来做简单匹配
KEYWORDS = [
    "校园卡", "一卡通", "完美校园", "挂失", "补办", "充值", "消费限额", "密码",
    "选课", "教务系统", "WebVPN", "重修", "学分", "课表", "通识", "必修",
    "图书馆", "借书", "借阅", "续借", "自习", "座位", "公众号", "数据库",
    "宿舍", "报修", "后勤", "宿管", "维修", "空调", "水龙头", "门锁",
    "学费", "缴费", "住宿费", "医保", "助学贷款", "财务", "欠费", "毕业",
]


def load_paragraphs():
    """
    读取 data 目录下的 txt 资料，并按段落拆开。
    返回格式：[{"source": "文件名", "content": "段落内容"}, ...]
    """
    paragraphs = []

    if not DATA_DIR.exists():
        return paragraphs

    for file_path in DATA_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        parts = text.split("\n\n")

        for part in parts:
            content = part.strip()
            if content != "":
                paragraphs.append({
                    "source": file_path.name,
                    "content": content,
                })

    return paragraphs


def calculate_score(question, content, source):
    """
    计算问题和某个资料段落的相关程度。
    分数越高，说明这个段落越可能包含答案。
    """
    score = 0

    for keyword in KEYWORDS:
        if keyword in question and keyword in content:
            score = score + 10
        elif keyword in question and keyword in source:
            score = score + 6

    for char in question:
        if char.strip() != "" and char in content:
            score = score + 1

    return score


def search_campus_data(question):
    """
    从校园资料中查找最相关的段落。
    这是一个轻量版检索，后续可以替换为正式 RAG 检索。
    """
    paragraphs = load_paragraphs()
    best_score = 0
    best_item = None

    for item in paragraphs:
        score = calculate_score(question, item["content"], item["source"])
        if score > best_score:
            best_score = score
            best_item = item

    if best_item is None or best_score < 5:
        return "抱歉，校园资料中没有找到相关信息。你可以换个说法再问一次，例如：校园卡怎么挂失？图书馆能借几本书？选课系统怎么进？"

    answer = best_item["content"] + "\n\n资料来源：" + best_item["source"]
    return answer


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
    当前先用 data 目录下的 txt 资料做简单检索。
    后续组长接入 RAG 后，可以把 search_campus_data() 替换成正式检索和大模型生成。
    """
    question = req.question.strip()

    if question == "":
        return ChatResponse(answer="请输入问题后再发送。")

    answer = search_campus_data(question)
    return ChatResponse(answer=answer)


if __name__ == "__main__":
    # 启动服务，浏览器访问 http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
