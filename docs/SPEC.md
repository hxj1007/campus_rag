# 校园资料智能问答助手 —— 技术规范文档（SPEC）

> 文档版本：v1.0
> 编写日期：2026 年 9 月
> 编写人：李政达（组长）

---

## 一、技术栈选型

| 层 | 选型 | 版本 | 选型理由 |
|---|---|---|---|
| 语言 | Python | 3.12 | 课程教学语言，生态成熟 |
| 后端框架 | FastAPI | 0.135.1 | 轻量、异步、自动生成 Swagger 文档（对应老师 Part 5） |
| ASGI 服务器 | Uvicorn | 0.46.0 | FastAPI 官方推荐 |
| 数据校验 | Pydantic | 2.12.5 | FastAPI 自带，定义请求/响应模型 |
| 环境变量 | python-dotenv | 1.2.1 | 读取 `.env` 里的密钥 |
| AI 框架 | LangChain | 1.2.12 | 提供 RAG 完整工具链（对应老师 Part 6） |
| LangChain 子包 | langchain-core / langchain-openai / langchain-chroma / langchain-community / langchain-text-splitters | 见 requirements.txt | 分别负责消息、模型、向量库、加载器、切分 |
| 大模型 | DeepSeek（deepseek-chat） | — | 国产、便宜、OpenAI 兼容接口 |
| 嵌入模型 | 硅基流动 BAAI/bge-large-zh-v1.5 | — | 免费额度、中文语义效果好 |
| 向量数据库 | Chroma | 1.1.0（chromadb） | 本地持久化、免部署、LangChain 原生支持 |
| 前端 | 原生 HTML + CSS + JavaScript | — | 单页够用，无需框架 |
| 数据存储 | 无关系型数据库，多轮记忆用内存 | — | 最小化依赖，符合课程范围 |

### 选型补充说明

- **为什么大模型和嵌入模型分开**：DeepSeek 不提供 embedding（向量化）接口，所以嵌入用硅基流动的 bge 模型；两者都是 OpenAI 兼容接口，用 `langchain_openai` 的 `ChatOpenAI` / `OpenAIEmbeddings` 都能对接。
- **为什么不用 MySQL**：本项目数据量小、场景简单，多轮对话用内存列表即可（进程重启即清空），不引入数据库能大幅降低部署和讲解成本。老师 Part 5 的数据库章节本项目明确跳过。

---

## 二、整体项目目录结构

```
campus_rag/
├── main.py                     # FastAPI 入口（谭存林）
├── requirements.txt            # 依赖列表
├── .env.example                # 密钥模板（复制成 .env 使用）
├── .gitignore                  # 排除 .env / __pycache__ / .idea / chroma_db
├── README.md                   # 项目说明 + 环境搭建
├── AGENTS.md                   # AI 协作规范
├── docs/                       # 项目文档（本目录）
│   ├── 需求调研.md
│   ├── 需求规格说明书.md
│   └── SPEC.md
├── static/
│   └── index.html              # 前端聊天页（高星晨）
├── data/
│   └── 示例资料.txt            # 校园资料（高星晨收集）
├── chroma_db/                  # 生成的向量库（本地，不提交）
└── app/
    ├── __init__.py
    ├── rag/                    # RAG 核心链路（组长 李政达）
    │   ├── __init__.py         # 定义 BASE_DIR / DATA_DIR / CHROMA_DIR，加载 .env
    │   ├── document_loader.py  # 环节1：加载
    │   ├── text_splitter.py    # 环节2：切分
    │   ├── embedding.py        # 环节3：向量化
    │   ├── vector_store.py     # 环节4：存储 + 读取
    │   ├── retriever.py        # 环节5：检索
    │   └── build_index.py      # 一键建库入口
    ├── llm/                    # 模型接入 + 提示词 + 记忆（王皓阳）
    │   ├── __init__.py
    │   ├── llm.py              # 大模型实例 get_llm()
    │   ├── embeddings.py       # embedding 实例 get_embeddings()
    │   ├── generator.py        # 生成主入口 generate()
    │   ├── memory.py           # 多轮记忆 ConversationMemory
    │   └── prompt.py           # 提示词 SYSTEM_PROMPT + format_context
    ├── api/                    # 接口路由（谭存林，待补）
    │   └── __init__.py
    └── models/                 # 数据模型（谭存林，待补）
        └── __init__.py
```

---

## 三、数据模型

> 本项目**不使用关系型数据库**，因此没有"数据表"，用**内存数据结构 + Pydantic 实体类**来表示数据。下面逐一说明。

### 3.1 请求 / 响应模型（Pydantic 实体类）

定义在 `main.py`（后续可下沉到 `app/models/`）：

```python
from pydantic import BaseModel

# 请求模型：前端发来的数据格式
class ChatRequest(BaseModel):
    question: str          # 用户的问题

# 响应模型：返回给前端的数据格式
class ChatResponse(BaseModel):
    answer: str            # 助手的回答
```

**待扩展字段（为多轮记忆服务）**：

```python
class ChatRequest(BaseModel):
    question: str
    session_id: str = ""   # 会话标识，用于多轮记忆隔离

class ChatResponse(BaseModel):
    answer: str
    session_id: str = ""   # 回传会话标识，前端后续请求带上它
```

> 说明：目前前端 `index.html` 只发送 `{question}`，尚未带 `session_id`。要让"多轮记忆"真正生效，需要前端和后端同时补上 `session_id` 的传递（见第五节"待统一事项"）。

### 3.2 多轮对话记忆数据结构

定义在 `app/llm/memory.py` 的 `ConversationMemory` 类，核心是一个**字典**：

```python
# 结构：{ session_id: [ {"role":"user"/"assistant", "content":"..."}, ... ] }
sessions = {
    "session_abc123": [
        {"role": "user",      "content": "图书馆能借几本书？"},
        {"role": "assistant", "content": "本科生每次最多借阅 5 本，借期 30 天。"},
        {"role": "user",      "content": "那能续借吗？"},
        # ...
    ]
}
```

规则：
- 按 `session_id` 隔离不同会话；
- 每个会话最多保留 `max_turns`（默认 5）轮，超出的自动丢弃最旧的（`_trim` 实现，一轮 = 2 条消息）。

### 3.3 RAG 文档数据结构（数据流）

RAG 链路中的数据形态变化：

```
data/示例资料.txt（原始文本）
        │  TextLoader.load()
        ▼
Document 列表（每篇 txt 一个 Document，含 page_content 文本 + metadata 元信息）
        │  RecursiveCharacterTextSplitter.split_documents()
        ▼
chunk 文本块（约 500 字/块，重叠 50 字，仍是 Document 列表）
        │  OpenAIEmbeddings.embed()
        ▼
向量（浮点数数组，维度由 bge-large-zh 决定，1024 维）
        │  Chroma.from_documents()
        ▼
chroma_db/ 本地向量库（chroma.sqlite3 + 索引文件）
```

### 3.4 Chroma 向量库存储结构

- 持久化目录：`chroma_db/`
- 内部文件：`chroma.sqlite3`（元数据 + 文本） + 向量索引子目录
- 写入用 `Chroma.from_documents(documents=, embedding=, persist_directory=)`
- 读取用 `Chroma(persist_directory=, embedding_function=)`（注意两处参数名不同）

---

## 四、关键技术点

### 4.1 RAG 五环节串联

完整链路（已实现于 `app/rag/`）：

```
load_documents()  →  split_documents()  →  get_embeddings()  →  build_vector_store()  →  retrieve()
   加载              切分                 向量化                存储                      检索
```

`app/rag/build_index.py` 的 `build_index()` 把前四步串起来，运行一次即可建库；`retrieve()` 负责查询时检索。

### 4.2 中文文本切分

`RecursiveCharacterTextSplitter` 的 `separators` 按**中文语义优先级**从大到小：

```python
separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""]
chunk_size=500      # 每块最大 500 字
chunk_overlap=50    # 相邻块重叠 50 字，避免一句话被硬截断
```

### 4.3 bge embedding 接入的特殊处理

bge 模型不是 OpenAI 官方模型，OpenAIEmbeddings 默认会做 token 长度检查导致误报，必须关闭：

```python
OpenAIEmbeddings(
    model="BAAI/bge-large-zh-v1.5",
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url=os.getenv("SILICONFLOW_BASE_URL"),
    check_embedding_ctx_length=False,   # 关键：跳过长度检查
)
```

### 4.4 幻觉控制（提示词工程）

在系统提示词里给模型立规矩（`app/llm/prompt.py` 的 `SYSTEM_PROMPT`）：

1. 校园知识类问题**只按参考资料回答**，不编造；
2. 资料中没有 → 明确回复"抱歉，校园资料中没有找到相关信息……"；
3. 多轮记忆类问题（"我叫什么名字"）优先看历史对话；
4. 寒暄聊天可以正常友好回应。

### 4.5 多轮记忆

- `ConversationMemory` 用内存字典按 `session_id` 隔离，超限自动截断；
- `history_to_messages()` 把历史转成 `HumanMessage` / `AIMessage` 列表；
- `generator.generate()` 组装消息顺序：`SystemMessage(带上下文) + 历史消息 + 当前问题`。

### 4.6 CORS 跨域

前端 `index.html` 直接 `fetch` 访问 `http://127.0.0.1:8000/chat`，属跨域请求，必须加 CORS 中间件：

```python
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
```

### 4.7 密钥管理

- 密钥全部放 `.env`（`DEEPSEEK_API_KEY`、`SILICONFLOW_API_KEY` 等）；
- 代码里用 `os.getenv(...)` 读取，不写死；
- `.env` 加入 `.gitignore`，绝不提交到 GitHub。

---



## 五、启动与部署方式

### 5.1 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置密钥（复制 .env.example 为 .env 并填入密钥）

# 3. 建向量库（首次，资料准备好后运行一次）
python -m app.rag.build_index

# 4. 启动后端
python main.py        # 访问 http://127.0.0.1:8000

# 5. 打开前端
#    浏览器打开 static/index.html
```

### 5.2 部署方式（本课程阶段）

- **本阶段**：本地单机运行，后端 + 前端在同一台电脑。
- **后续可选**：用 Uvicorn 部署到云服务器（`uvicorn main:app --host 0.0.0.0 --port 8000`），前端通过 Nginx 托管，非本期重点。
