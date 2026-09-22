# app/llm/memory.py
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain_core")
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")
warnings.filterwarnings("ignore", category=DeprecationWarning)


class ConversationMemory:
    """
    基于内存列表的多轮对话记忆
    - 按 session_id 隔离不同用户的会话
    - 每个会话保留最近 N 轮对话
    - 超出自动丢弃最旧的（参考 Part6 第3章 3.2 对话历史优化）
    """

    def __init__(self, max_turns: int = 5):
        """
        :param max_turns: 每个会话最多保留几轮对话（默认5轮）
        """
        self.max_turns = max_turns
        # {session_id: [{"role":"user"/"assistant", "content":"..."}]}
        self.sessions = {}

    def add_user(self, session_id: str, content: str):
        """向指定会话追加一条用户消息"""
        self._ensure_session(session_id)
        self.sessions[session_id].append({"role": "user", "content": content})
        self._trim(session_id)

    def add_assistant(self, session_id: str, content: str):
        """向指定会话追加一条 AI 回复"""
        self._ensure_session(session_id)
        self.sessions[session_id].append({"role": "assistant", "content": content})
        self._trim(session_id)

    def get_history(self, session_id: str):
        """获取指定会话的历史（返回副本，避免外部误改）"""
        return list(self.sessions.get(session_id, []))

    def clear(self, session_id: str):
        """清空指定会话的历史"""
        self.sessions.pop(session_id, None)

    def _ensure_session(self, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []

    def _trim(self, session_id: str):
        """每轮=2条消息，最多保留 max_turns*2 条"""
        max_msgs = self.max_turns * 2
        if len(self.sessions[session_id]) > max_msgs:
            self.sessions[session_id] = self.sessions[session_id][-max_msgs:]


def history_to_messages(history):
    """
    把 history 列表转为 LangChain 消息对象列表
    参考 Part6 第3章 2「消息的类型」
    :param history: [{"role":"user"/"assistant","content":"..."}]
    :return: [HumanMessage/AIMessage, ...]
    """
    from langchain_core.messages import HumanMessage, AIMessage

    messages = []
    for h in history:
        if h["role"] == "user":
            messages.append(HumanMessage(content=h["content"]))
        elif h["role"] == "assistant":
            messages.append(AIMessage(content=h["content"]))
    return messages