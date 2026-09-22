# app/llm/prompt.py
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_core")
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_core.prompts import ChatPromptTemplate


# 系统提示词：定义角色 + RAG 回答规则 + 多轮记忆规则
SYSTEM_PROMPT = """你是一个校园资料智能问答助手。请优先根据历史对话和下面的【参考资料】来回答用户的问题。

【参考资料】
{context}

回答要求：
1. 首先查看历史对话，如果用户问的是关于之前对话中出现过的信息（如"我叫什么名字""我刚才问了什么"等），请根据历史对话回答。
2. 关于校园知识类问题（如选课、图书馆、校园卡、宿舍、学费等），只根据参考资料回答，不要编造资料中没有的内容。
3. 如果参考资料中没有相关的校园信息，请直接回答："抱歉，校园资料中没有找到相关信息，建议咨询学校相关部门。"
4. 对于用户自我介绍、寒暄、聊天等非校园知识类问题，可以正常友好回应。
5. 回答要简洁、准确、友好，用中文回答。
"""

# 用户提示词模板
USER_PROMPT = "{question}"


def build_prompt():
    """
    构建 RAG 提示词模板（LangChain 标准用法）
    :return: ChatPromptTemplate 实例
    """
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("user", USER_PROMPT),
    ])


def format_context(docs):
    """
    把检索到的文档块列表拼成上下文字符串
    :param docs: Document 列表 或 str 列表（来自组长的 retriever）
    :return: 拼接后的字符串
    """
    if not docs:
        return "（无相关参考资料）"
    parts = []
    for i, doc in enumerate(docs, 1):
        # 兼容 Document 对象和纯字符串
        text = doc.page_content if hasattr(doc, "page_content") else str(doc)
        parts.append(f"【资料{i}】{text}")
    return "\n\n".join(parts)